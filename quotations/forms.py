from django.forms.models import ModelForm
from . import models

class QuotationForm(ModelForm):
    class Meta:
        model = models.Quotation
        fields = ['customer', 'vehiculeYearMake', 'vehiculeModel',
                  'vehiculeNumber', 'vehiculePrice', 'coverages']
