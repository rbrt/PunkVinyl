from django import forms


class SearchForm(forms.Form):
    form_field = forms.CharField(max_length=50, required = True)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=50, required=True)