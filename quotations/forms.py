from django.forms.models import ModelForm
from django import forms
from django.template.defaultfilters import default


class QuotationForm(forms.Form):
    """
    Form for Quotation create API Call
    View : :view:`QuotationCreateView`
    """

    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    vehiculeYearMake = forms.IntegerField(label='Vehicule Year Make')
    vehiculeModel = forms.CharField(max_length=80, label='Vehicule Model')
    vehiculeNumber = forms.CharField(max_length=30, label='Vehicule Number')
    vehiculePrice = forms.DecimalField(min_value=30_000, initial=100_000,
                                       label='Vehicule Price')
    covWind = forms.BooleanField(required=False, label='Wind Coverage')
    covPass = forms.BooleanField(required=False, label='Passenger Coverage')
    covFlood = forms.BooleanField(required=False, label='Flood coverage')
