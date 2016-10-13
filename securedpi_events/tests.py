from django.test import TestCase
from django.contrib.auth.models import User
from securedpi_events.models import Event
from securedpi_locks.models import Lock
from django.urls import reverse
from securedpi_locks.tests import SetupTestCase


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


class EventViewTestCase(SetupTestCase):
    """Define test class for event view."""
    def setUp(self):
        """Define setup for tests."""
        self.setUp = super(EventViewTestCase, self).setUp()
        self.url = reverse('events', kwargs={'pk': self.lock1.pk})
        self.template = 'securedpi_events/events.html'
        self.event1 = Event(lock_id=self.lock1.pk, serial=self.lock1.serial,
                            action='unlock', mtype='manual')
        self.event1.save()
        self.event2 = Event(lock_id=self.lock1.pk, serial=self.lock1.serial,
                            action='unlock', mtype='manual')
        self.event2.save()
        self.response = self.client.get(self.url)

    def test_auth_user_has_access_to_events(self):
        """Prove that response code is 200 for auth users."""
        self.assertEquals(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render page."""
        self.assertTemplateUsed(self.response, self.template)

    def test_events_in_context(self):
        """Prove that 'events' are in response context."""
        self.assertIn('events', self.response.context)

    def test_correct_number_of_events_page(self):
        """Prove that correct number of events renders on the events page."""
        self.assertEqual(self.response.context['events'].count(), 2)
