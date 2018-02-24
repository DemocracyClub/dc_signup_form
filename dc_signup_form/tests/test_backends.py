from django.test import TestCase
from dc_signup_form.backends import LocalDbBackend
from dc_signup_form.signup_server.views import SignupQueue


class TestLocalDbBackend(TestCase):

    def test_valid(self):
        backend = LocalDbBackend()

        # ensure the queue is tempty before we start
        self.assertEqual(0, len(SignupQueue.objects.all()))

        backend.submit({'email': 'foo@bar.baz'}, ['main_list'])

        # now there should be a record in the queue
        self.assertEqual(1, len(SignupQueue.objects.all()))

    def test_invalid(self):
        backend = LocalDbBackend()
        with self.assertRaises(KeyError):
            backend.submit({'foo': 'bar'}, ['main_list'])
