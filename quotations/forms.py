from django.forms.models import ModelForm
from django import forms
from django.template.defaultfilters import default


class QuotationForm(forms.Form):
    """
    Form for Quotation create API Call
    View : `:view:`QuotationCreateView
    """

    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    vehiculeYearMake = forms.IntegerField()
    vehiculeModel = forms.CharField(max_length=80)
    vehiculeNumber = forms.CharField(max_length=30)
    vehiculePrice = forms.DecimalField(min_value=30_000)
    covWind = forms.BooleanField(required=False)
    covPass = forms.BooleanField(required=False)
    covFlood = forms.BooleanField(required=False)
