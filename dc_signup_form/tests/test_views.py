import json

from django.test import Client, TestCase

from dc_signup_form.constants import (
    MAILING_LIST_FORM_PREFIX,
)

from .test_forms import add_data_prefix
from .utils import mocked_eventbridge


class TestView(TestCase):
    def test_get_mailing_list_form_view(self):
        c = Client()
        response = c.get("/emails/mailing_list/")
        self.assertEqual(200, response.status_code)
        expected_strings = [
            '<input id="id_mailing_list_form-source_url" name="mailing_list_form-source_url" type="hidden" value="/emails/mailing_list/" />',
            '<input id="id_mailing_list_form-main_list" name="mailing_list_form-main_list" type="hidden" value="True" />',
            '<input type="text" name="mailing_list_form-full_name" autocomplete="off" pattern="[^@]+" title="Please enter your full name, not your email address." maxlength="1000" class="" required="" id="id_mailing_list_form-full_name">',
            '<input type="email" name="mailing_list_form-email" maxlength="255" class="" required="" id="id_mailing_list_form-email">',
        ]
        for string in expected_strings:
            with self.subTest(string=string):
                self.assertContains(response, string, html=True)

    def test_post_mailing_list_form_view_valid(self):
        with mocked_eventbridge() as get_events:
            self.assertEqual(0, len(get_events()))
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
            self.assertEqual(1, len(get_events()))

    def test_source_url(self):
        with mocked_eventbridge() as get_events:
            # add a test to make sure the source url is
            # being passed through correctly
            self.assertEqual(0, len(get_events()))
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
            events = get_events()
            self.assertEqual(1, len(events))
            self.assertEqual(
                "/emails/mailing_list/",
                json.loads(events[0]["Body"])["detail"]["attribs"]["source_url"],
            )

    def test_post_mailing_list_form_view_invalid(self):
        with mocked_eventbridge() as get_events:
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
            self.assertIn('<div class="ds-error">', str(response.content))
            self.assertEqual(0, len(get_events()))
