from django.forms import forms

class SearchForm(forms.Form):
    form_field = forms.CharField(max_length=50, required = True)