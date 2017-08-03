from django.conf.urls import url

from .views import SignupFormView

urlpatterns = [
    url(
        r'^$',
        SignupFormView.as_view(),
        name='email_signup_view'),
]
