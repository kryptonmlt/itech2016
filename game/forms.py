from django import forms
from game.models import City
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('name',)
