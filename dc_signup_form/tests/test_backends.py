import boto3
from django.test import TestCase
from moto import mock_events

from dc_signup_form.backends import LocalDbBackend, EventBridgeBackend
from dc_signup_form.signup_server.views import SignupQueue


class TestLocalDbBackend(TestCase):
    def test_valid(self):
        backend = LocalDbBackend()

        # ensure the queue is tempty before we start
        self.assertEqual(0, len(SignupQueue.objects.all()))

        backend.submit({"email": "foo@bar.baz"}, ["main_list"])

        # now there should be a record in the queue
        self.assertEqual(1, len(SignupQueue.objects.all()))

    def test_invalid(self):
        backend = LocalDbBackend()
        with self.assertRaises(KeyError):
            backend.submit({"foo": "bar"}, ["main_list"])


class TestEventBridgeBackend(TestCase):
    @mock_events
    def test_valid(self):
        bus_arn_name = "arn:testing"
        client = boto3.client("events", region_name="eu-west-2")
        client.create_event_bus(Name=bus_arn_name)

        backend = EventBridgeBackend(source="UnitTest", bus_arn="arn:testing")
        backend.submit({"email": "foo@bar.baz", "full_name": "Test Face"}, ["main_list"])
