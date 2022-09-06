import requests
import json
from django.conf import settings
from dc_signup_form.signup_server.models import SignupQueue


class TestBackend:
    def submit(self, data, mailing_lists):
        print(
            {
                "data": data,
                "mailing_lists": mailing_lists,
            }
        )


class LocalDbBackend:
    def submit(self, data, mailing_lists):
        record = SignupQueue(
            email=data["email"], data=data, mailing_lists=mailing_lists
        )
        record.save()


class RemoteDbBackend:
    def submit(self, data, mailing_lists):
        key = getattr(settings, "EMAIL_SIGNUP_API_KEY", "")
        url = getattr(settings, "EMAIL_SIGNUP_ENDPOINT", "")

        headers = {"Authorization": key}

        payload = {
            "data": data,
            "mailing_lists": mailing_lists,
        }

        r = requests.post(url, data=json.dumps(payload), headers=headers)
        r.raise_for_status()
