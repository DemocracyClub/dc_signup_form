import django
import unittest
from distutils.version import StrictVersion
from django.test import TestCase
try:
    from dc_signup_form.signup_server.views import SignupQueue
    from dc_signup_form.signup_server.management.commands.sync_to_sendgrid import Command
except ImportError:
    pass


@unittest.skipIf(StrictVersion(django.get_version()) < '1.9.0',
    'LocalDbBackend requires Django 1.9 or later')
class TestSyncCommand(TestCase):

    def test_get_new_users_no_data(self):
        command = Command()
        users = command.get_new_users(['main_list'])
        self.assertEqual(0, len(list(users)))

    def test_get_new_users_with_data(self):
        command = Command()
        records = [
            SignupQueue(
                email='foo@example.com',
                data={'foo': 'bar'},
                mailing_lists=['main_list']
            ),
            SignupQueue(
                email='bar@example.com',
                data={'foo': 'bar'},
                mailing_lists=['main_list']
            ),
            SignupQueue(
                email='baz@example.com',
                data={'foo': 'bar'},
                mailing_lists=['some_other_list']
            )
        ]
        for record in records:
            record.save()
        users = command.get_new_users(['main_list'])
        self.assertEqual(2, len(list(users)))

    def test_get_new_users_with_test_user(self):
        command = Command()
        records = [
            SignupQueue(
                email='foo@example.com',
                data={'foo': 'bar'},
                mailing_lists=['main_list']
            ),
            SignupQueue(
                email='bar@example.com',
                data={'foo': 'bar'},
                mailing_lists=['main_list']
            ),
            SignupQueue(
                email='baz@example.com',
                data={'foo': 'bar'},
                mailing_lists=['some_other_list']
            ),
            SignupQueue(
                email='testy.mctest@democracyclub.org.uk',
                data={'foo': 'bar'},
                mailing_lists=['main_list']
            )
        ]
        for record in records:
            record.save()
        users = command.get_new_users(['main_list'])
        self.assertEqual(2, len(list(users)))
