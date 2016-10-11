from django.test import TestCase
from django.contrib.auth.models import User
from securedpi_events.models import Event
from securedpi_locks.models import Lock
from django.urls import reverse


class EventTestCase(TestCase):
    """Create test class for Event model."""
    def setUp(self):
        """Set up a fake user with a lock."""
        self.user = User(username='test')
        self.user.set_password('test')
        self.user.save()
        self.lock = Lock(
            user=self.user,
            title='lock1',
            location='codefellows',
            serial='pi12345')
        self.lock.save()
        self.event = Event(
            lock_id = self.lock,
            serial = 'test_serial'
        )
        self.event.save()

    def test_event_exists(self):
        """Prove the event exists."""
        self.assertTrue(self.event is not None)

    def test_attributes_correct(self):
        """Prove the attributes of an event are correct."""
        attr_vals = [
            ('lock_id', self.lock),
            ('serial', 'test_serial'),
            ('action_taken', ''),
            ('method', ''),
            ('photo', None)
        ]
        for key, val in attr_vals:
            self.assertEqual(getattr(self.event, key), val)
    
    def test_lock_has_event(self):
        """Prove that a lock has 1 event."""
        self.assertTrue(self.lock.events.count(), 1)
