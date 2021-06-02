from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login
from django.views.generic import ListView, DetailView, CreateView
from api import models
from . import forms


class QuotationListView(ListView):

    """
    List of all the :model:`Quotation` made by the connected :model:`Customer`
    Click on a row to get the quotation detail
    :template:`quotation/quotation_list.html`
    """

    model = models.Quotation
    template_name = 'quotations/quotation_list.html'

    def get(self, request):
        quotations = models.Quotation.objects.filter(
            customer__username=request.user.username)
        return render(request, self.template_name, {'quotations': quotations,
                                                    'userConnected': request.user.username})


class QuotationDetailView(DetailView):
    """
    Display an invidicual :model:`Quotation`
    TODO email generation from this page
    template name :template:`quotations/quotation.html`
    """

    model = models.Quotation
    template_name = 'quotations/quotation.html'

    def get(self, request, id):
        """
        get metod to retrieve the quotation
        TODO replace by an API call
        """
        quot = models.Quotation.objects.get(id=id)
        return render(request, self.template_name, {'quotation': quot})


class QuotationCreateView(CreateView):
    """
    Form for :model:`Quotation creation`
    Automtically generate the email
    TODO do this in the detail view
    """

    template_name = 'quotations/create.html'
    #createform = forms.QuotationForm()

    def post(self, request):
        self.createform = forms.QuotationForm(request.POST)
        if self.createform.is_valid():
            cust = self.get_by_email_or_create(
                request)
            t = models.Quotation(
                customer=cust,
                vehiculeModel=self.createform.cleaned_data['vehiculeModel'],
                vehiculeYearMake=self.createform.cleaned_data['vehiculeYearMake'],
                vehiculeNumber=self.createform.cleaned_data['vehiculeNumber'],
                vehiculePrice=self.createform.cleaned_data['vehiculePrice'],
                covWind=self.createform.cleaned_data['covWind'],
                covPass=self.createform.cleaned_data['covPass'],
                covFlood=self.createform.cleaned_data['covFlood'],
            )
            t.calculate_and_save()
            t.send_email()
        else:
            return render(request, self.template_name, {'form': self.createform})
        return HttpResponseRedirect('/quotation/' + str(t.id))

    def get_by_email_or_create(self, request):
        """
        Retrieve the `:model:`Customer with the email inputed or create a new one
        """
        mail = self.createform.cleaned_data['email']
        cust = models.Customer.objects.filter(username__icontains=mail)
        if cust:
            login(request, cust.first())
            return cust.first()

        # No user ? create one
        cust = models.Customer.objects.create(
            username=mail,
            last_name=self.createform.cleaned_data['name'],
            phone=self.createform.cleaned_data['phone']
        )
        cust.set_password('Tigerlab@2021')
        cust.save()
        login(request, cust)
        return cust

    def get(self, request):
        """
        Initialize the form for `:model:`Quotation creation
        """
        return render(request, self.template_name, {'form': self.createform})
