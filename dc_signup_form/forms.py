from django import forms
from django.core.validators import RegexValidator

from .constants import ELECTION_REMINDERS_FORM_PREFIX, MAILING_LIST_FORM_PREFIX


def emails_not_accepted(value):
    if '@' in value:
        raise forms.ValidationError("Please enter your full name, not your email address.")

class EmailSignupForm(forms.Form):
    full_name = forms.CharField(
        required=True, 
        max_length=1000, 
        label="Full Name",
        validators=[emails_not_accepted],
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'pattern': '[^@]+', 'title': 'Please enter your full name, not your email address.'})
    )
    email = forms.EmailField(required=True, max_length=255, label="Email")
    source_url = forms.CharField(widget=forms.HiddenInput())

class ElectionRemindersSignupForm(EmailSignupForm):

    prefix = ELECTION_REMINDERS_FORM_PREFIX

    main_list = forms.BooleanField(
        required=False,
        initial=False,
        label="Subscribe to the Democracy Club mailing list",
    )
    election_reminders = forms.BooleanField(initial=True, widget=forms.HiddenInput())


class MailingListSignupForm(EmailSignupForm):

    prefix = MAILING_LIST_FORM_PREFIX

    main_list = forms.BooleanField(initial=True, widget=forms.HiddenInput())
