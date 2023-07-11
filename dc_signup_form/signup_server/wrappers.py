import requests
import json
from django.conf import settings


class DCSendGridWrapper:

    BASE_URL = "https://api.sendgrid.com/v3"
    SENDGRID_LISTS = {
        "main_list": 1246575,
        "election_reminders": 1342244,
    }

    # list of properties we shouldn't pass to SendGrid
    # because we don't have a custom field for it
    FIELD_BLACKLIST = ["source_url"]

    def __init__(self):
        key = getattr(settings, "SENDGRID_API_KEY", "")
        self.headers = {"Authorization": "Bearer " + key}

    def get_users_payload(self, users):
        payload = []
        for user in users:
            data = {}
            for key in user:
                if key not in self.FIELD_BLACKLIST:
                    data[key] = user[key]
            payload.append(data)
        return payload

    def add_users(self, payload):
        url = self.BASE_URL + "/contactdb/recipients"
        r = requests.post(url, data=json.dumps(payload), headers=self.headers) 
        r.raise_for_status()
        return r.json()

    def get_contact_lists(self):
        url = self.BASE_URL + "/contactdb/lists"
        r = requests.get(url, headers=self.headers)
        # if we get a non-2xx status code, just raise it
        r.raise_for_status()
        return r.json()

    def add_users_to_lists(self, payload, mailing_list):
        url = self.BASE_URL + "/contactdb/lists/{list_id}/recipients".format(
            list_id=mailing_list
        )
        r = requests.post(url, data=json.dumps(payload), headers=self.headers)
        # if we get a non-2xx status code, just raise it
        r.raise_for_status()
        # if success response payload wil be empty so there is no return val

class SendGridAPIError(ValueError): 
    pass