from django import forms
from . import models



class CustomerForm(forms.Form):
    class Meta:
        model = models.Customer
        fields = ['name']


class QuotationForm(forms.Form):
    #vehiculeYearMake=forms.IntegerField(label="Vehicule Year Make", required=False)
    class Meta:
        model = models.Quotation
        fields = ['vehiculeYearMake', 'vehiculeModel',
                  'VehiculeNumber', 'vehiculePrice']
