from django.test import TestCase
from django.contrib.auth.models import User
from securedpi_locks.models import SecuredpiLock


class SecurepiLockTestCase(TestCase):
    """Create test class for SecuredpiLock model."""
    def setUp(self):
        """Set up a fake user."""
        self.user = User(username='test')
        self.user.set_password('test')
        self.user.save()
        self.lock = SecuredpiLock(
            user=self.user,
            label='lock1',
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
            ('label', 'lock1'),
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
