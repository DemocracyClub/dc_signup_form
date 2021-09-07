from django.urls import re_path

from .forms import ElectionRemindersSignupForm, MailingListSignupForm
from .views import SignupFormView

app_name = 'dc_signup_form'
urlpatterns = [
    re_path(
        r'^mailing_list/$',
        SignupFormView.as_view(
            template_name='email_form/mailing_list_form_view.html',
            form_class=MailingListSignupForm,
        ),
        name='mailing_list_signup_view'),
    re_path(
        r'^election_reminders/$',
        SignupFormView.as_view(
            template_name='email_form/election_reminders_form_view.html',
            form_class=ElectionRemindersSignupForm,
            get_vars=['postcode'],
            thanks_message="Thanks for joining. We'll send you a reminder when there's an upcoming election in your area",
        ),
        name='election_reminders_signup_view'),
]
