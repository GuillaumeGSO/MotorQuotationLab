from api.models import Customer
from django.contrib.auth.forms import UserCreationForm
from django import forms


class RegisterForm(UserCreationForm):
    phone = forms.CharField()

    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone']
