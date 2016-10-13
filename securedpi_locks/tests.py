from django.test import TestCase
from django.contrib.auth.models import User
from securedpi_locks.models import Lock
from django.urls import reverse


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
    Define class for tests setup. All other test classes inherit
    form this class.
    """
    def setUp(self):
        """Define setup for tests."""
        self.user = User(username='test')
        self.user.save()
        self.client.force_login(user=self.user)
        self.lock1 = Lock(
            user=self.user,
            name='lock1',
            location='codefellows',
            serial='pi12345')
        self.lock1.save()
        self.lock2 = Lock(
            user=self.user,
            name='lock2',
            location='codefellows',
            serial='pi1234512345')
        self.lock2.save()
        self.expected1 = 'href="{}"'.format(
            reverse('manual_lock', kwargs={'pk': self.lock1.pk, 'action': 'lock'}))
        self.expected2 = 'href="{}"'.format(
            reverse('manual_unlock', kwargs={'pk': self.lock1.pk, 'action': 'unlock'}))


class EditLockTestCase(SetupTestCase):
    """Define test case class for lock editing."""
    def setUp(self):
        """Set up for the test case class."""
        self.setUp = super(EditLockTestCase, self).setUp()
        self.url = reverse('edit_lock', kwargs={'pk': self.lock1.pk})
        self.response = self.client.get(self.url)
        self.template = 'securedpi_locks/edit_lock.html'
        self.data = {
            "name": 'lock1_updated',
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
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))

    def test_lock_info_updated(self):
        """Prove that lock info was updated."""
        self.assertEqual(self.lock1.name, 'lock1')
        self.assertEqual(self.lock1.location, 'codefellows')
        self.assertEqual(self.lock1.serial,'pi12345')
        self.assertEqual(self.lock1.description, '')
        self.client.post(self.url, self.data)
        lock1 = Lock.objects.filter(user=self.user).first()
        self.assertEqual(lock1.name, 'lock1_updated')
        self.assertEqual(lock1.description, 'closet')
        self.assertEqual(lock1.location, 'codefellows')
        self.assertEqual(lock1.serial,'pi12345')

    def test_number_of_locks_didnt_change(self):
        """
        Prove that after updating a lock, the total number of locks
        didn't change.
        """
        # number of locks before update
        count1 = self.user.locks.all().count()
        self.client.post(self.url, self.data)
        # number of locks after update
        count2 = self.user.locks.all().count()
        self.assertEqual(count1, count2)
