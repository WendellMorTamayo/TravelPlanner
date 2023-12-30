from django.forms import ModelForm, PasswordInput
from .models import User
from django import forms


class UserRegistrationForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(widget=forms.TextInput)
    last_name = forms.CharField(widget=forms.TextInput)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    contact_number = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'date_of_birth',
            'contact_number',
        ]
