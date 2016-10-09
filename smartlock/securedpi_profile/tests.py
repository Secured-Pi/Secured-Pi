from django.test import TestCase
from django.contrib.auth.models import User
from securedpi_profile.models import SecuredpiProfile
from django.urls import reverse


class SecurepiProfileTestCase(TestCase):
    """Create test class for SecuredpiProfile model."""
    def setUp(self):
        """Set up a fake user."""
        self.user = User(username='test')
        self.user.set_password('test')
        self.user.save()

    def test_user_exists(self):
        """Prove the user exists."""
        self.assertTrue(self.user is not None)

    def test_username(self):
        """Prove the username is correct."""
        self.assertEqual(self.user.username, 'test')

    def test_profile_exists(self):
        """Prove that a profile is automatically created for a new user."""
        self.assertTrue(self.user.profile is not None)

    def test_profile_is_attached_to_right_user(self):
        """Prove that the profileis attached to the right user."""
        self.assertEqual(self.user.profile.user.username, 'test')

    def test_profile_attributes(self):
        """Prove that SecuredpiProfile model has expected attributes."""
        attrs = ['first_name', 'last_name', 'address', 'email']
        for attr in attrs:
            self.assertTrue(hasattr(self.user.profile, attr))
