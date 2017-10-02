import django
from distutils.version import StrictVersion
from django.test import TestCase
from dc_signup_form.backends import LocalDbBackend
try:
    from dc_signup_form.signup_server.views import SignupQueue
except ImportError:
    pass
from django.core.exceptions import ImproperlyConfigured


class TestLocalDbBackend(TestCase):

    def test_valid(self):
        backend = LocalDbBackend()

        if StrictVersion(django.get_version()) < '1.9.0':
            with self.assertRaises(ImproperlyConfigured):
                backend.submit({'email': 'foo@bar.baz'}, ['main_list'])
        else:
            # ensure the queue is tempty before we start
            self.assertEqual(0, len(SignupQueue.objects.all()))

            backend.submit({'email': 'foo@bar.baz'}, ['main_list'])

            # now there should be a record in the queue
            self.assertEqual(1, len(SignupQueue.objects.all()))

    def test_invalid(self):
        backend = LocalDbBackend()

        if StrictVersion(django.get_version()) < '1.9.0':
            with self.assertRaises(ImproperlyConfigured):
                backend.submit({'foo': 'bar'}, ['main_list'])
        else:
            with self.assertRaises(KeyError):
                backend.submit({'foo': 'bar'}, ['main_list'])
