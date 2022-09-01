from django.urls import include, re_path

from dc_signup_form.forms import ElectionRemindersSignupForm, MailingListSignupForm
from dc_signup_form.views import SignupFormView


email_patterns = [
    re_path(
        r"^mailing_list/$",
        SignupFormView.as_view(
            template_name="email_form/mailing_list_form_view.html",
            form_class=MailingListSignupForm,
            backend="local_db",
        ),
        name="mailing_list_signup_view",
    ),
    re_path(
        r"^election_reminders/$",
        SignupFormView.as_view(
            template_name="email_form/election_reminders_form_view.html",
            form_class=ElectionRemindersSignupForm,
            get_vars=["postcode"],
            thanks_message="Thanks for joining. We'll send you a reminder when there's an upcoming election in your area",
            backend="local_db",
        ),
        name="election_reminders_signup_view",
    ),
]


urlpatterns = [
    re_path(r"^emails/", include((email_patterns, "dc_signup_form"))),
]
