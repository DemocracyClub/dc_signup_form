from django.conf.urls import url

from .views import email_signup

urlpatterns = [
    url(r'^$',
        email_signup,
        name='email_signup_api_endpoint'),
]
