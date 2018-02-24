import json
from django.test import TestCase, RequestFactory
from dc_signup_form.signup_server.views import SignupQueue, Token
from dc_signup_form.signup_server.views import email_signup


class TestSignupView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_no_auth_header(self):
        req = self.factory.post(
            '/foo/bar',
            content_type='application/json',
            data=json.dumps({'foo': 'bar'}),
        )
        response = email_signup(req)
        self.assertEqual(403, response.status_code)

    def test_bad_auth_header(self):
        req = self.factory.post(
            '/foo/bar',
            content_type='application/json',
            data=json.dumps({'foo': 'bar'}),
            HTTP_AUTHORIZATION='foobar'
        )
        response = email_signup(req)
        self.assertEqual(403, response.status_code)

    def test_valid(self):
        # ensure the queue is tempty before we start
        self.assertEqual(0, len(SignupQueue.objects.all()))

        token = Token()
        token.app_name = 'myapp'
        token.save()

        req = self.factory.post(
            '/foo/bar',
            content_type='application/json',
            data=json.dumps({
                'data': {'email': 'foo@bar.baz'},
                'mailing_lists': ['main_list']
            }),
            HTTP_AUTHORIZATION=token.token
        )
        response = email_signup(req)
        self.assertEqual(201, response.status_code)

        # now there should be a record in the queue
        self.assertEqual(1, len(SignupQueue.objects.all()))
