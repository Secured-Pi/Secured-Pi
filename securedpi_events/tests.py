from django.test import TestCase
from django.contrib.auth.models import User
from securedpi_events.models import Event
from securedpi_locks.models import Lock
from django.urls import reverse


class EventTestCase(TestCase):
    """Create test class for Event model."""
    def setUp(self):
        """Set up a fake user with a lock."""
        self.event = Event(
            lock_id='123',
            serial='test_serial',
            token='test_token'
        )
        self.event.save()

    def test_event_exists(self):
        """Prove the event exists."""
        self.assertTrue(self.event is not None)

    def test_attributes_correct(self):
        """Prove the attributes of an event are correct."""
        attr_vals = [
            ('lock_id', '123'),
            ('serial', 'test_serial'),
            ('token', 'test_token'),
            ('action_taken', ''),
            ('method', ''),
            ('photo', None)
        ]
        for key, val in attr_vals:
            self.assertEqual(getattr(self.event, key), val)
