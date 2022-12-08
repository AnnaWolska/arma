
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

    labels = {
        "username": "nazwa użytkownika:",
        "email": "e-mail:",
        "first_name": "imię:",
        "last_name": "nazwisko:",
        "password1": "hasło:",
        "password2": "powtórzenie hasła:"
    }