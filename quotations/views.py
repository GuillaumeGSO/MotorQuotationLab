from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from . import models
from . import forms


class QuotationListView(ListView):

    model = models.Quotation
    """ model = models.Quotation
    template_name = 'quotations/quotation_list.html'

    @login_required
    def get(self, request):
        return render(request, reversed('quotation_list'))

    def get_queryset(self):
        return models.Quotation.objects.filter(customer=self.request.user) """


class QuotationDetailView(DetailView):

    model = models.Quotation
    template_name = 'quotations/quotation.html'

    # @login_required
    def get(self, request, id):
        quot = models.Quotation.objects.get(id=id)
        return render(request, self.template_name, {'quotation': quot})


class QuotationCreateView(CreateView):

    template_name = 'quotations/create.html'
    createform = forms.QuotationForm()

    def post(self, request):
        self.createform = forms.QuotationForm(request.POST)
        if self.createform.is_valid():
            cust = self.get_by_email_or_create(
                request, self.createform.cleaned_data["email"])
            t = models.Quotation(
                customer=cust,
                vehiculeModel=self.createform.cleaned_data["vehiculeModel"],
                vehiculeYearMake=self.createform.cleaned_data["vehiculeYearMake"],
                vehiculeNumber=self.createform.cleaned_data["vehiculeNumber"],
                vehiculePrice=self.createform.cleaned_data["vehiculePrice"],
                covWind=self.createform.cleaned_data["covWind"],
                covPass=self.createform.cleaned_data["covPass"],
                covFlood=self.createform.cleaned_data["covFlood"],
            )
        t.calculate_and_save()
        t.send_email()
        return HttpResponseRedirect("/quotation/" + str(t.id))

    def get_by_email_or_create(self, request, mail):
        cust = models.Customer.objects.filter(email__icontains=mail)
        if cust:
            return cust.first()
        cust = models.Customer.objects.create(username="TODO", email=mail,
                                              phone="ddd", password="Tigerlab@2021")
        login(request, cust)
        return cust

    def get(self, request):
        return render(request, self.template_name, {'form': self.createform})
