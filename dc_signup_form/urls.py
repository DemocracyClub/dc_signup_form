from django.conf.urls import url

from .views import SignupFormView

urlpatterns = [
    url(
        r'^$',
        SignupFormView.as_view(
            mailing_lists=['main list']
        ),
        name='email_signup_view'),
]
