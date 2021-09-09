from django.urls import re_path

from .views import email_signup

urlpatterns = [
    re_path(r'^$',
        email_signup,
        name='email_signup_api_endpoint'),
]
