import requests
import json
from django.conf import settings


class TestWrapper:
    def submit(self, data, mailing_lists):
        print({
            'data': data,
            'mailing_lists': mailing_lists,
        })


class DCSendGridWrapper:

    BASE_URL = 'https://api.sendgrid.com/v3'
    SENDGRID_LISTS = {
        'main list': 1246575,
        'election reminders': 1342244,
    }

    # list of properties we shouldn't pass to SendGrid
    # because we don't have a custom field for it
    FIELD_BLACKLIST = ['source_url']

    def __init__(self):
        key = getattr(settings, 'SENDGRID_API_KEY', '')
        self.headers = {
            'Authorization': 'Bearer ' + key
        }

    def get_user_payload(self, data):
        payload = {}
        for key in data:
            if key not in self.FIELD_BLACKLIST:
                payload[key] = data[key]
        return [payload]

    def add_user(self, payload):
        url = self.BASE_URL + '/contactdb/recipients'
        r = requests.post(url,
            data=json.dumps(payload),
            headers=self.headers
        )

        # if we get a non-2xx status code, just raise it
        r.raise_for_status()

        response = r.json()
        # We can submit multiple users at once. Some records might work
        # some some might not, so sometimes we get a 201 response with errors
        if response['error_count'] > 0:
            raise requests.exceptions.HTTPError(
                response['errors'][0]['message'])

        return response['persisted_recipients'][0]

    def get_contact_lists(self):
        url = self.BASE_URL + '/contactdb/lists'
        r = requests.get(url,
            headers=self.headers
        )
        # if we get a non-2xx status code, just raise it
        r.raise_for_status()
        return r.json()

    def add_user_to_list(self, user_id, mailing_list):
        url = self.BASE_URL +\
            "/contactdb/lists/{list_id}/recipients/{recipient_id}".format(
                list_id=mailing_list,
                recipient_id=user_id
            )
        r = requests.post(url,
            headers=self.headers
        )
        # if we get a non-2xx status code, just raise it
        r.raise_for_status()
        # if success response payload wil be empty so there is no return val

    def submit(self, data, mailing_lists):
        user_id = self.add_user(self.get_user_payload(data))
        for mailing_list in mailing_lists:
            if mailing_list in self.SENDGRID_LISTS:
                self.add_user_to_list(
                    user_id,
                    self.SENDGRID_LISTS[mailing_list]
                )
            else:
                raise KeyError(
                    "'%s' not found in SENDGRID_LISTS" % mailing_list)
