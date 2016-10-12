from django.test import TestCase
from django.contrib.auth.models import User
from securedpi_events.models import Event
from securedpi_locks.models import Lock
from django.urls import reverse


class EventTestCase(TestCase):
    """Create test class for Event model."""
    def setUp(self):
        """Setup for test."""
        self.event = Event(
            lock_id='123',
            serial='test_serial',
            mtype='manual',
            action='lock'
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
            ('status', ''),
            ('mtype', 'manual'),
            ('action', 'lock'),
            ('photo', None)
        ]
        for key, val in attr_vals:
            self.assertEqual(getattr(self.event, key), val)
