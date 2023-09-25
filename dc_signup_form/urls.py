from django.urls import re_path

from .forms import MailingListSignupForm
from .views import SignupFormView

app_name = "dc_signup_form"
urlpatterns = [
    re_path(
        r"^mailing_list/$",
        SignupFormView.as_view(
            template_name="email_form/mailing_list_form_view.html",
            form_class=MailingListSignupForm,
        ),
        name="mailing_list_signup_view",
    ),
]
