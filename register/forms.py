from quotations.models import Customer
from django.contrib.auth.forms import UserCreationForm
from django import forms


class RegisterForm(UserCreationForm):
    phone = forms.CharField()
    password1 = ""
    password2 = ""
    class Meta:
        model = Customer
        fields=['username', 'email', 'phone']