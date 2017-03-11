from django.test import TestCase
from django.contrib.auth.models import User
from securedpi_locks.models import Lock
from securedpi_events.models import Event
from django.urls import reverse
from unittest import mock


class LockTestCase(TestCase):
    """Create test class for Lock model."""
    def setUp(self):
        """Set up a fake user."""
        self.user = User(username='test')
        self.user.set_password('test')
        self.user.save()
        self.lock = Lock(
            user=self.user,
            name='lock1',
            location='codefellows',
            serial='pi12345')
        self.lock.save()

    def test_lock_exists(self):
        """Prove the lock exists."""
        self.assertTrue(self.lock is not None)

    def test_attributes_correct(self):
        """Prove the attributes of a lock are correct."""
        attr_vals = [
            ('user', self.user),
            ('name', 'lock1'),
            ('location', 'codefellows'),
            ('description', ''),
            ('serial', 'pi12345'),
            ('status', 'unlocked'),
            ('facial_recognition', False),
            ('is_active', False)
        ]
        for key, val in attr_vals:
            self.assertEqual(getattr(self.lock, key), val)

    def test_user_has_lock(self):
        """Prove that the user has 1 lock."""
        self.assertTrue(self.user.locks.count(), 1)


class LockAccessCase(TestCase):
    """
    Make sure unauth users redirected to login page when trying accessing
    'locks/' urls.
    """
    def test_no_access_to_events_if_unath(self):
        """Prove redirection to the login page."""
        urls = [
            reverse('edit_lock', kwargs={'pk': 1}),
            reverse('delete_lock', kwargs={'pk': 1}),
            reverse('manual_unlock', kwargs={'pk': 1}),
            reverse('manual_lock', kwargs={'pk': 1}),
        ]
        login_url = reverse('auth_login')
        for url in urls:
            response = self.client.get(url, follow=True)
            expected_url = '{}?next={}'.format(login_url, url)
            expected = (expected_url, 302)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.redirect_chain), 1)
            self.assertTupleEqual(response.redirect_chain[0], expected)


class SetupTestCase(TestCase):
    """
    Define class for tests setup.
    EditLockTestCase and DeleteLockTestCase classes inherit form this class.
    """
    def setUp(self):
        """Define setup for tests."""
        self.user = User(username='test')
        self.user.save()
        self.client.force_login(user=self.user)
        self.lock = Lock(
            user=self.user,
            name='test_lock',
            location='codefellows',
            serial='pi12345')
        self.lock.save()


class EditLockTestCase(SetupTestCase):
    """Define test case class for lock editing."""
    def setUp(self):
        """Set up for the test case class."""
        self.setUp = super(EditLockTestCase, self).setUp()
        self.url = reverse('edit_lock', kwargs={'pk': self.lock.pk})
        self.response = self.client.get(self.url)
        self.template = 'securedpi_locks/edit_lock.html'
        self.data = {
            "name": 'lock_updated',
            "location": "codefellows",
            "description": "closet",
            "serial": "pi12345"
        }

    def test_auth_user_have_access_to_lock_edit(self):
        """Prove that auth user has access to the lock edit."""
        self.assertEqual(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render edit lock page."""
        self.assertTemplateUsed(self.response, self.template)

    def test_form_present_in_context(self):
        """Prove that form is present in response context."""
        self.assertIn('form', self.response.context)

    def test_redirect_on_update_from_edit_lock_page(self):
        """Prove redirection to dashboard page after updating a lock."""
        response = self.client.post(self.url, self.data)
        self.assertRedirects(
            response,
            expected_url=reverse('dashboard'),
            status_code=302,
            target_status_code=200)

    def test_lock_info_updated(self):
        """Prove that lock info was updated."""
        self.assertEqual(self.lock.name, 'test_lock')
        self.assertEqual(self.lock.location, 'codefellows')
        self.assertEqual(self.lock.serial, 'pi12345')
        self.assertEqual(self.lock.description, '')
        self.client.post(self.url, self.data)
        lock = Lock.objects.filter(user=self.user).first()
        self.assertEqual(lock.name, 'lock_updated')
        self.assertEqual(lock.description, 'closet')
        self.assertEqual(lock.location, 'codefellows')
        self.assertEqual(lock.serial, 'pi12345')

    def test_number_of_locks_didnt_change(self):
        """
        Prove that after updating a lock, the total number of locks
        didn't change.
        """
        # number of locks before an update
        count1 = self.user.locks.all().count()
        self.client.post(self.url, self.data)
        # number of locks after an update
        count2 = self.user.locks.all().count()
        self.assertEqual(count1, count2)

    def test_delete_btn_present(self):
        """Make sure <Delete> button is present."""
        url = reverse('delete_lock', kwargs={'pk': self.lock.pk})
        expected = 'href="{}"'.format(url)
        self.assertContains(self.response, expected)


class DeleteLockTestCase(SetupTestCase):
    """Define class to test delete lock view."""
    def setUp(self):
        """Setup for testing."""
        self.setUp = super(DeleteLockTestCase, self).setUp()
        self.url = reverse('delete_lock', kwargs={'pk': self.lock.pk})
        self.response = self.client.get(self.url)
        self.template = 'securedpi_locks/lock_confirm_delete.html'

    def test_auth_user_have_access_to_delete_edit(self):
        """Prove that auth user has access to the lock edit."""
        self.assertEqual(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that the right template is used to render delete lock page."""
        self.assertTemplateUsed(self.response, self.template)

    def test_correct_lock_name_displayed(self):
        """
        Make sure the correct lock name is displayed
        on the delete confirm page.
        """
        self.assertContains(self.response, 'test_lock')

    def delete_btn_works(self):
        """Make sure <Delete> btn works."""
        self.assertEquals(self.user.locks.count(), 1)
        self.client.post(self.url)
        self.assertEquals(self.user.locks.count(), 0)

    def test_redirection_to_dashboard_after_deletion(self):
        """Prove redirection to dashboard after deletion of a lock."""
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            expected_url=reverse('dashboard'),
            status_code=302,
            target_status_code=200)


class ManualActionTestCase(SetupTestCase):
    """Define class for testing manual_action()."""
    def setUp(self):
        """Setup for testing."""
        self.setup = super(ManualActionTestCase, self).setUp()
        self.url1 = reverse(
            'manual_unlock',
            kwargs={'pk': self.lock.pk, 'action': 'unlock'}
            )
        self.url2 = reverse(
            'manual_lock',
            kwargs={'pk': self.lock.pk, 'action': 'lock'}
            )

    @mock.patch('requests.post')
    def test_manual_unlock_creates_event(self, request_mock):
        """Prove that an event is created after clicking on <Unlock> button."""
        self.assertEqual(Event.objects.all().count(), 0)
        self.client.get(self.url1)
        self.assertEqual(Event.objects.all().count(), 1)

    @mock.patch('requests.post')
    def test_manual_lock_creates_event(self, request_mock):
        """Prove that an event is created after clicking on <Lock> button."""
        self.assertEqual(Event.objects.all().count(), 0)
        self.client.get(self.url2)
        self.assertEqual(Event.objects.all().count(), 1)

    @mock.patch('requests.post')
    def test_attrs_of_created_unlock_event(self, request_mock):
        """Prove that the created event has expected attributes."""
        self.client.get(self.url1)
        self.assertEqual(Event.objects.first().lock_id, str(self.lock.pk))
        self.assertEqual(Event.objects.first().action, 'unlock')
        self.assertEqual(Event.objects.first().mtype, 'manual')
        self.assertEqual(Event.objects.first().status, 'failed')
        self.assertEqual(Event.objects.first().serial, str(self.lock.serial))

    @mock.patch('requests.post')
    def test_attrs_of_created_lock_event(self, request_mock):
        """Prove that the created event has expected attributes."""
        self.client.get(self.url2)
        self.assertEqual(Event.objects.first().lock_id, str(self.lock.pk))
        self.assertEqual(Event.objects.first().action, 'lock')
        self.assertEqual(Event.objects.first().mtype, 'manual')
        self.assertEqual(Event.objects.first().status, 'failed')
        self.assertEqual(Event.objects.first().serial, str(self.lock.serial))

    @mock.patch('requests.post')
    def test_manual_action_redirect_to_dashboard(self, request_mock):
        """Prove redirect to dashboard after manual unlock."""
        urls = [self.url1, self.url2]
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(
                response,
                expected_url=reverse('dashboard'),
                status_code=302,
                target_status_code=200)

    @mock.patch('requests.post')
    def test_lock_status_becomes_pending_after_unlock(self, request_mock):
        """
        Prove that the status of a lock changes to 'pending' after
        clicking <Unlock> button.
        """
        self.lock.status = 'locked'
        self.lock.save()
        self.assertEqual(self.lock.status, 'locked')
        self.client.get(self.url1)
        self.assertEqual(Lock.objects.get(pk=self.lock.pk).status, 'pending')

    @mock.patch('requests.post')
    def test_lock_status_becomes_pending_after_lock(self, request_mock):
        """
        Prove that the status of a lock changes to 'pending' after
        clicking <Lock> button.
        """
        self.assertEqual(self.lock.status, 'unlocked')
        self.client.get(self.url2)
        self.assertEqual(Lock.objects.get(pk=self.lock.pk).status, 'pending')
