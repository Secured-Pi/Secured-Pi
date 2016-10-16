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

    def test_profile_exists(self):
        """Prove that a profile is automatically created for a new user."""
        self.assertTrue(self.user.profile is not None)

    def test_profile_is_attached_to_right_user(self):
        """Prove that the profileis attached to the right user."""
        self.assertEqual(self.user.profile.user.username, 'test')

    def test_profile_attributes(self):
        """Prove that SecuredpiProfile model has expected attributes."""
        attrs = ['first_name', 'last_name', 'address', 'phone_number']
        for attr in attrs:
            self.assertTrue(hasattr(self.user.profile, attr))


class ProfileAccessCase(TestCase):
    """
    Make sure unauth users redirected to login page when trying accessing
    'profile/' urls.
    """
    def test_no_access_to_events_if_unath(self):
        """Prove redirection to the login page."""
        urls = [
            reverse('profile'),
            reverse('edit_profile', kwargs={'pk': 1}),
        ]
        login_url = reverse('auth_login')
        for url in urls:
            response = self.client.get(url, follow=True)
            expected_url = '{}?next={}'.format(login_url, url)
            expected = (expected_url, 302)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.redirect_chain), 1)
            self.assertTupleEqual(response.redirect_chain[0], expected)


class ProfileViewTestCase(TestCase):
    """Define class to test the profile view."""
    def setUp(self):
        """Define setup for the test class."""
        self.user = User(username='test')
        self.user.save()
        self.client.force_login(user=self.user)
        self.url = reverse('profile')
        self.response = self.client.get(self.url)
        self.template = 'securedpi_profile/profile.html'

    def test_auth_user_have_access_to_profile_view(self):
        """Prove that auth user has access to the profile view."""
        self.assertEqual(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render profile page."""
        self.assertTemplateUsed(self.response, self.template)

    def test_profile_edit_button_present(self):
        """Prove that <edit profile> button is present."""
        expected = 'href="{}"'.format(reverse(
            'edit_profile', kwargs={'pk': self.user.pk}))
        self.assertContains(self.response, expected)

    def test_profile_info_displayed_correctly(self):
        attr = ['First Name', 'Last Name', 'Address', 'Phone']
        for x in attr:
            self.assertContains(self.response, x)


class EditProfileTestCase(TestCase):
    """Define test case class for profile editing."""
    def setUp(self):
        """Set up for the test case class."""
        self.user = User(username='test')
        self.user.save()
        self.client.force_login(user=self.user)
        self.complete_profile()
        self.url = reverse('edit_profile', kwargs={'pk': self.user.pk})
        self.response = self.client.get(self.url)

    def complete_profile(self):
        """Complete user's profile via <edit progfile> page."""
        data = {
            'user': self.user,
            'first_name': 'name',
            'last_name': 'lastname',
            'address': 'address',
            'phone_number': 'number'
        }
        self.client.post(
            reverse('edit_profile', kwargs={'pk': self.user.pk}),
            data
        )

    def test_auth_user_have_access_to_profile_edit(self):
        """Prove that auth user has access to the album edit."""
        self.assertEqual(self.response.status_code, 200)

    def test_right_template_is_used(self):
        """Prove that right template is used to render edit profile page."""
        self.assertTemplateUsed(
            self.response,
            'securedpi_profile/securedpiprofile_form.html'
        )

    def test_form_present_in_context(self):
        """Prove that form is present in response context."""
        self.assertIn('form', self.response.context)

    def test_redirect_on_update_from_edit_profile_page(self):
        """
        Prove redirection to the profile page after successfully updating
        the profile.
        """
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            expected_url=reverse('profile'),
            status_code=302,
            target_status_code=200)

    def test_updated_info_shows_up(self):
        """Prove that updated profile info shows up on profile page."""
        # info before update
        attr = ['name', 'lastname', 'address', 'number']
        response = self.client.get(reverse('profile'))
        for x in attr:
            self.assertContains(response, x)
        # updating info
        data = {
            'user': self.user,
            'first_name': 'updated1',
            'last_name': 'updated2',
            'address': 'updated3',
            'phone_number': 'updated4'
        }
        self.client.post(
            reverse('edit_profile', kwargs={'pk': self.user.pk}),
            data
        )
        # info after update
        attr = ['updated1', 'updated2', 'updated3', 'updated4']
        response = self.client.get(reverse('profile'))
        for x in attr:
            self.assertContains(response, x)
