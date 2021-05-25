from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from . import models
from . import forms


class QuotationListView(ListView):

    model = models.Quotation
    template_name = 'quotations/quotation_list.html'

    # @login_required(login_url='/register/login/')
    def get(self, request):
        quotations = models.Quotation.objects.filter(
            customer__username=request.user.username)
        return render(request, self.template_name, {'quotations': quotations,
                                                    'userConnected': request.user.username})


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
        return HttpResponseRedirect('/quotation/' + str(t.id))

    def get_by_email_or_create(self, request):
        mail = self.createform.cleaned_data['email']
        cust = models.Customer.objects.filter(username__icontains=mail)
        if cust:
            return cust.first()
        # No user
        cust = models.Customer.objects.create(
            username=mail,
            last_name=self.createform.cleaned_data['name'],
            phone=self.createform.cleaned_data['phone'],
            password='Tigerlab@2021')
        login(request, cust)
        return cust

    def get(self, request):
        return render(request, self.template_name, {'form': self.createform})
