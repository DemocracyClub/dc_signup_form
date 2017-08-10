from django import forms


class EmailSignupForm(forms.Form):
    full_name = forms.CharField(required=True, max_length=1000,
        label="Name")
    email = forms.EmailField(required=True, max_length=255,
        label="Email")
    source_url = forms.CharField(widget=forms.HiddenInput())


class ElectionRemindersSignupForm(EmailSignupForm):
    main_list = forms.BooleanField(
        required=False,
        initial=False,
        label='Subscribe to the Democracy Club mailing list')
    election_reminders = forms.BooleanField(
        initial=True,
        widget=forms.HiddenInput())


class MailingListSignupForm(EmailSignupForm):
    main_list = forms.BooleanField(
        initial=True,
        widget=forms.HiddenInput())
