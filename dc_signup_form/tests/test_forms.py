from django.test import TestCase
from dc_signup_form.forms import (
    ElectionRemindersSignupForm, MailingListSignupForm)


class TestForms(TestCase):

    def test_mailing_list_form_valid(self):
        form = MailingListSignupForm(data={
            'full_name': 'Chad Fernandez',
            'email': 'chad.fernandez@democracyclub.org.uk',
            'source_url': 'http://foo.bar/baz',
            'main_list': True,
        })
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_mailing_list_invalid(self):
        form = MailingListSignupForm(data={
            'full_name': '',  # empty field
            'email': 'foo',  # not an email
            'source_url': 'http://foo.bar/baz',
            'main_list': True,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)
        self.assertIn('This field is required.', form.errors['full_name'])
        self.assertIn('email', form.errors)
        self.assertIn('Enter a valid email address.', form.errors['email'])

    def test_mailing_list_required_fields(self):
        form = MailingListSignupForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)
        self.assertIn('This field is required.', form.errors['full_name'])
        self.assertIn('email', form.errors)
        self.assertIn('This field is required.', form.errors['email'])
        self.assertIn('source_url', form.errors)
        self.assertIn('This field is required.', form.errors['source_url'])
        self.assertIn('main_list', form.errors)
        self.assertIn('This field is required.', form.errors['main_list'])

    def test_election_reminders_form_valid(self):
        form = ElectionRemindersSignupForm(data={
            'full_name': 'Chad Fernandez',
            'email': 'chad.fernandez@democracyclub.org.uk',
            'source_url': 'http://foo.bar/baz',
            'main_list': False,
            'election_reminders': True,
        })
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_election_reminders_invalid(self):
        form = ElectionRemindersSignupForm(data={
            'full_name': '',  # empty field
            'email': 'foo',  # not an email
            'source_url': 'http://foo.bar/baz',
            'main_list': True,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)
        self.assertIn('This field is required.', form.errors['full_name'])
        self.assertIn('email', form.errors)
        self.assertIn('Enter a valid email address.', form.errors['email'])

    def test_election_reminders_required_fields(self):
        form = ElectionRemindersSignupForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)
        self.assertIn('This field is required.', form.errors['full_name'])
        self.assertIn('email', form.errors)
        self.assertIn('This field is required.', form.errors['email'])
        self.assertIn('source_url', form.errors)
        self.assertIn('This field is required.', form.errors['source_url'])
        self.assertIn('election_reminders', form.errors)
        self.assertIn('This field is required.', form.errors['election_reminders'])
