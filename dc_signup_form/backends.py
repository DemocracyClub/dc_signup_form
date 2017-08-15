import django
import requests
import json
from distutils.version import StrictVersion
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
try:
    from dc_signup_form.signup_server.models import SignupQueue
except ImportError:
    pass


class TestBackend:
    def submit(self, data, mailing_lists):
        print({
            'data': data,
            'mailing_lists': mailing_lists,
        })


class LocalDbBackend:

    def submit(self, data, mailing_lists):
        try:
            record = SignupQueue(
                email=data['email'],
                data=data,
                mailing_lists=mailing_lists
            )
            record.save()
        except NameError:
            if StrictVersion(django.get_version()) < '1.9.0':
                raise ImproperlyConfigured(
                    'LocalDbBackend requires Django 1.9 or later')
            else:
                raise


class RemoteDbBackend:

    def submit(self, data, mailing_lists):
        key = getattr(settings, 'EMAIL_SIGNUP_API_KEY', '')
        url = getattr(settings, 'EMAIL_SIGNUP_ENDPOINT', '')

        headers = {
            'Authorization': key
        }

        payload = {
            'data': data,
            'mailing_lists': mailing_lists,
        }

        r = requests.post(url,
            data=json.dumps(payload),
            headers=headers
        )
        r.raise_for_status()
