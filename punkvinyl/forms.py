from django import forms
from django.core.exceptions import ValidationError


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

    def clean(self):
        import pdb; pdb.set_trace()
        if None == self.image:
            raise ValidationError("No image link supplied")
        if None == self.band:
            raise ValidationError("No band name supplied")
        if None == self.link:
            raise ValidationError("No link supplied")
        if None == self.album:
            raise ValidationError("No album name supplied")
        if None == self.price:
            raise ValidationError("No price supplied")
        if None == self.vinyl:
            raise ValidationError("No vinyl size supplied")
