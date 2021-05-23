from django.forms.models import ModelForm
from . import models

class QuotationForm(ModelForm):
    class Meta:
        model = models.Quotation
        fields = ['vehiculeYearMake', 'vehiculeModel',
                  'vehiculeNumber', 'vehiculePrice', 'coverages']
