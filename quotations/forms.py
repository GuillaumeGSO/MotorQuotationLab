from django import forms

class CreateNewQuotation(forms.Form):
    vehiculeYearMake=forms.IntegerField(label="Vehicule Year Make", required=False)
    vehiculeModel = forms.CharField(label="Vehicule Model", max_length=80)
    vehiculePrice=forms.NumberInput()
