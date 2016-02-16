from django import forms
from game.models import Account
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('picture',)
