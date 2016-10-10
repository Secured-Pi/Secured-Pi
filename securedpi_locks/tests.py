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
            title='lock1',
            location='codefellows',
            raspberry_pi_id='pi12345')
        self.lock.save()

    def test_lock_exists(self):
        """Prove the lock exists."""
        self.assertTrue(self.lock is not None)

    def test_attributes_correct(self):
        """Prove the attributes are correct."""
        attr_vals = [
            ('user', self.user),
            ('title', 'lock1'),
            ('location', 'codefellows'),
            ('description', ''),
            ('raspberry_pi_id', 'pi12345'),
            ('web_cam_id', ''),
            ('is_locked', False)
        ]
        for key, val in attr_vals:
            self.assertEqual(getattr(self.lock, key), val)

    def test_user_has_lock(self):
        """Prove that the user has 1 lock."""
        self.assertTrue(self.user.locks.count(), 1)


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
            title='lock1',
            location='codefellows',
            raspberry_pi_id='pi12345')
        self.lock1.save()
        self.lock2 = Lock(
            user=self.user,
            title='lock2',
            location='codefellows',
            raspberry_pi_id='pi1234512345')
        self.lock2.save()


class DashboardViewTestCase(SetupTestCase):
    """Define test class for Dashboard view."""
    def setUp(self):
        """Define setup for tests."""
        self.setUp = super(DashboardViewTestCase, self).setUp()
        self.url = reverse('dashboard')
        self.response = self.client.get(self.url)
        self.template = 'securedpi_locks/dashboard.html'

    def test_auth_user_has_access_to_dashboard(self):
        """Prove that response code is 200 for auth users."""
        self.assertEquals(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render page."""
        self.assertTemplateUsed(self.response, self.template)

    def test_locks_in_context(self):
        """Prove that 'locks' are in response context."""
        self.assertIn('locks', self.response.context)

    def test_correct_number_of_locks_on_dashboard(self):
        """Prove that correct number of locks renders on the dashboard."""
        self.assertEqual(self.response.context['locks'].count(), 2)
