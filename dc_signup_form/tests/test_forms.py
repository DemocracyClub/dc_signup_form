from django.test import TestCase

from dc_signup_form.constants import (
    MAILING_LIST_FORM_PREFIX,
)
from dc_signup_form.forms import MailingListSignupForm


def add_data_prefix(prefix, data):
    return {
        "{}-{}".format(prefix, k): v
        for k, v in data.items()
        if not str(v).startswith(k)
    }


class TestForms(TestCase):
    def test_mailing_list_form_valid(self):
        data = add_data_prefix(
            MAILING_LIST_FORM_PREFIX,
            {
                "full_name": "Chad Fernandez",
                "email": "chad.fernandez@democracyclub.org.uk",
                "source_url": "http://foo.bar/baz",
                "main_list": True,
            },
        )

        form = MailingListSignupForm(data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_mailing_list_invalid(self):
        data = add_data_prefix(
            MAILING_LIST_FORM_PREFIX,
            {
                "full_name": "",  # empty field
                "email": "foo",  # not an email
                "source_url": "http://foo.bar/baz",
                "main_list": True,
            },
        )
        form = MailingListSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("full_name", form.errors)
        self.assertIn("This field is required.", form.errors["full_name"])
        self.assertIn("email", form.errors)
        self.assertIn("Enter a valid email address.", form.errors["email"])

    def test_mailing_list_invalid_name(self):
        data = add_data_prefix(
            MAILING_LIST_FORM_PREFIX,
            {
                "full_name": "andrew@foo.com",  # @ in name
                "email": "andrew@foo.com",  # not an email
                "source_url": "http://foo.bar/baz",
                "main_list": True,
            },
        )
        form = MailingListSignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Please enter your full name, not your email address.",
            form.errors["full_name"],
        )

    def test_mailing_list_required_fields(self):
        form = MailingListSignupForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("full_name", form.errors)
        self.assertIn("This field is required.", form.errors["full_name"])
        self.assertIn("email", form.errors)
        self.assertIn("This field is required.", form.errors["email"])
        self.assertIn("source_url", form.errors)
        self.assertIn("This field is required.", form.errors["source_url"])
        self.assertIn("main_list", form.errors)
        self.assertIn("This field is required.", form.errors["main_list"])
