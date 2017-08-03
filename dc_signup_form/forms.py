from django import forms

class EmailSignupForm(forms.Form):
    name = forms.CharField(required=True, max_length=1000,
        label="Name")
    email = forms.EmailField(required=True, max_length=255,
        label="Email")
    source_url = forms.CharField(widget=forms.HiddenInput())
