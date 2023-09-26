from django.test import TestCase

from dc_signup_form.backends import EventBridgeBackend
from dc_signup_form.tests.utils import mocked_eventbridge


class TestEventBridgeBackend(TestCase):
    def test_valid(self):
        with mocked_eventbridge() as get_events:
            backend = EventBridgeBackend(
                source="UnitTest", bus_arn="arn:testing"
            )
            backend.submit(
                {"email": "foo@bar.baz", "full_name": "Test Face"},
                ["main_list"],
            )
            events = get_events()
        self.assertEqual(len(events), 1)
