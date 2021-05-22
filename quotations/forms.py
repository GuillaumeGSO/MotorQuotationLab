from django.forms.models import ModelForm
from . import models

class CustomerForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = ['name']


class QuotationForm(ModelForm):
    class Meta:
        model = models.Quotation
        fields = ['customer', 'vehiculeYearMake', 'vehiculeModel',
                  'vehiculeNumber', 'vehiculePrice', 'coverages']
