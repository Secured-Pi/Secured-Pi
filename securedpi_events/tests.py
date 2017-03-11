from django.test import TestCase
import factory
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
            ('status', 'failed'),
            ('mtype', 'manual'),
            ('action', 'lock'),
            ('photo', None)
        ]
        for key, val in attr_vals:
            self.assertEqual(getattr(self.event, key), val)


class EventAccessCase(TestCase):
    """
    Make sure unauth users redirected to login page when trying accessing
    events and delete_old-events routes.
    """
    def test_no_access_to_events_if_unath(self):
        """Prove redirection to the login page."""
        urls = [
            reverse('events', kwargs={'pk': 1}),
            reverse('delete_old_events', kwargs={'pk': 1})
        ]
        login_url = reverse('auth_login')
        for url in urls:
            response = self.client.get(url, follow=True)
            expected_url = '{}?next={}'.format(login_url, url)
            expected = (expected_url, 302)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.redirect_chain), 1)
            self.assertTupleEqual(response.redirect_chain[0], expected)


class EventFactory(factory.Factory):
    """Create an event factory."""
    class Meta:
        model = Event
    action = 'unlock'
    mtype = 'manual'
    serial = 'test'


class EventViewTestCase(TestCase):
    """Define test class for event view."""
    def setUp(self):
        """Define setup for tests."""
        self.user = User(username='test')
        self.user.save()
        self.lock = Lock(user=self.user, serial='1', name='a', location='b')
        self.lock.save()
        self.client.force_login(user=self.user)
        self.url = reverse('events', kwargs={'pk': self.lock.pk})
        self.template = 'securedpi_events/events.html'
        events = EventFactory.build_batch(10, lock_id=self.lock.pk)
        for event in events:
            event.save()
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
        self.assertEqual(self.response.context['events'].count(), 10)

    def test_delete_btn_present(self):
        """Prove that <delete_10_oldest_events> button present."""
        url = reverse('delete_old_events', kwargs={'pk': self.lock.pk})
        expected = 'href="{}"'.format(url)
        self.assertContains(self.response, expected)

    def test_delete_btn_works(self):
        """Prove <delete_10_oldest_events> btn works as expected."""
        count = Event.objects.filter(lock_id=self.lock.pk).count()
        self.assertEqual(count, 10)
        self.client.get(reverse('delete_old_events', kwargs={'pk': self.lock.pk}))
        count = Event.objects.filter(lock_id=self.lock.pk).count()
        self.assertEqual(count, 0)
