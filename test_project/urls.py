from django.urls import include, re_path

from dc_signup_form.forms import MailingListSignupForm
from dc_signup_form.views import SignupFormView


email_patterns = [
    re_path(
        r"^mailing_list/$",
        SignupFormView.as_view(
            template_name="email_form/mailing_list_form_view.html",
            form_class=MailingListSignupForm,
            backend="event_bridge",
            backend_kwargs={"source": "UnitTest", "bus_arn": "arn:testing"},
        ),
        name="mailing_list_signup_view",
    ),
]


urlpatterns = [
    re_path(r"^emails/", include((email_patterns, "dc_signup_form"))),
]
