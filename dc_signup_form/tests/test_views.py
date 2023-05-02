from django.test import Client, TestCase
from dc_signup_form.signup_server.models import SignupQueue

from dc_signup_form.constants import (
    MAILING_LIST_FORM_PREFIX,
    ELECTION_REMINDERS_FORM_PREFIX,
)

from .test_forms import add_data_prefix


class TestView(TestCase):
    def test_get_mailing_list_form_view(self):
        c = Client()
        response = c.get("/emails/mailing_list/")
        self.assertEqual(200, response.status_code)
        expected_strings = [
            '<input id="id_mailing_list_form-source_url" name="mailing_list_form-source_url" type="hidden" value="/emails/mailing_list/" />',
            '<input id="id_mailing_list_form-main_list" name="mailing_list_form-main_list" type="hidden" value="True" />',
            '<input class=" form-control" id="id_mailing_list_form-full_name" maxlength="1000" name="mailing_list_form-full_name" type="text" required />',
            '<input class=" form-control" id="id_mailing_list_form-email" maxlength="255" name="mailing_list_form-email" type="email" required />',
        ]
        for string in expected_strings:
            self.assertContains(response, string, html=True)

    def test_post_mailing_list_form_view_valid(self):
        self.assertEqual(0, len(SignupQueue.objects.all()))
        c = Client()
        response = c.post(
            "/emails/mailing_list/",
            add_data_prefix(
                MAILING_LIST_FORM_PREFIX,
                {
                    "source_url": "/emails/mailing_list/",
                    "main_list": True,
                    "full_name": "Chad Fernandez",
                    "email": "chad.fernandez@example.com",
                    "mailing_list_form": "",
                },
            ),
        )
        self.assertEqual(302, response.status_code)
        self.assertEqual(1, len(SignupQueue.objects.all()))

    def test_source_url (self):
        # add a test to make sure the source url is 
        # being passed through correctly
        self.assertEqual(0, len(SignupQueue.objects.all()))
        c = Client()
        response = c.post(
            "/emails/mailing_list/",
            add_data_prefix(
                MAILING_LIST_FORM_PREFIX,
                {
                    "source_url": "/emails/mailing_list/",
                    "main_list": True,
                    "full_name": "Chad Fernandez",
                    "email": "chad@test.com",
                    "mailing_list_form": "",
                },
            ),
        )
        self.assertEqual(302, response.status_code)
        self.assertEqual(1, len(SignupQueue.objects.all()))
        self.assertEqual("/emails/mailing_list/", SignupQueue.objects.all()[0].data["source_url"])
        



    
    def test_post_mailing_list_form_view_invalid(self):
        self.assertEqual(0, len(SignupQueue.objects.all()))
        c = Client()

        response = c.post(
            "/emails/mailing_list/",
            add_data_prefix(
                MAILING_LIST_FORM_PREFIX,
                {
                    "source_url": "/emails/mailing_list/",
                    "main_list": True,
                    "full_name": "Chad Fernandez",
                    "email": "",
                    "mailing_list_form": "",
                },
            ),
        )
        form = response.context[MAILING_LIST_FORM_PREFIX]
        self.assertFalse(form.is_valid())
        self.assertEqual(200, response.status_code)
        self.assertIn('<div class="form-group has-error">', str(response.content))
        self.assertEqual(0, len(SignupQueue.objects.all()))

    def test_get_election_reminders_form_view(self):
        c = Client()
        response = c.get("/emails/election_reminders/")
        self.assertEqual(200, response.status_code)
        expected_strings = [
            '<input id="id_election_reminders_form-source_url" name="election_reminders_form-source_url" type="hidden" value="/emails/election_reminders/" />',
            '<input id="id_election_reminders_form-election_reminders" name="election_reminders_form-election_reminders" type="hidden" value="True" />',
            '<input class=" form-control" id="id_election_reminders_form-full_name" maxlength="1000" name="election_reminders_form-full_name" type="text" required />',
            '<input class=" form-control" id="id_election_reminders_form-email" maxlength="255" name="election_reminders_form-email" type="email" required />',
            '<input id="id_election_reminders_form-main_list" name="election_reminders_form-main_list" type="checkbox" />',
        ]
        for string in expected_strings:
            self.assertContains(response, string, html=True)

    def test_post_election_reminders_form_view_valid(self):
        self.assertEqual(0, len(SignupQueue.objects.all()))
        c = Client()
        response = c.post(
            "/emails/election_reminders/",
            add_data_prefix(
                ELECTION_REMINDERS_FORM_PREFIX,
                {
                    "source_url": "/emails/election_reminders/",
                    "election_reminders": True,
                    "full_name": "Chad Fernandez",
                    "email": "chad.fernandez@example.com",
                    "main_list": False,
                    "election_reminders_form": "",
                },
            ),
        )
        self.assertEqual(302, response.status_code)
        self.assertEqual(1, len(SignupQueue.objects.all()))

    def test_post_election_reminders_form_view_invalid(self):
        self.assertEqual(0, len(SignupQueue.objects.all()))
        c = Client()
        response = c.post(
            "/emails/election_reminders/",
            {
                "source_url": "/emails/election_reminders/",
                "election_reminders": True,
                "full_name": "Chad Fernandez",
                "email": "",
                "main_list": False,
                "election_reminders_form": "",
            },
        )
        self.assertEqual(200, response.status_code)
        self.assertIn('<div class="form-group has-error">', str(response.content))
        self.assertEqual(0, len(SignupQueue.objects.all()))
