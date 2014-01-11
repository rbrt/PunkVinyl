from django import forms
from django.forms import ModelForm
from recordlist.models import Records


class SearchForm(forms.Form):
    form_field = forms.CharField(max_length=50, required=True)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput)


class BenForm(forms.Form):
    image = forms.CharField(max_length=50, required=True, label="Image Link")
    band = forms.CharField(max_length=50, required=True, label="Band Name")
    link = forms.CharField(max_length=50, required=True, label="Link to Page")
    album = forms.CharField(max_length=50, required=True, label="Album Name")
    price = forms.CharField(max_length=50, required=True, label="Price")
    vinyl = forms.CharField(max_length=50, required=True, label="Vinyl Size")
    sitename = forms.CharField(max_length=50, required=True, label="Distro Name")
