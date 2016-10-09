from django.test import TestCase
from django.urls import reverse
from django.core import mail


class HomePageTestCase(TestCase):
    """Create Home Page test case."""

    def setUp(self):
        """Set up response for home page test case."""
        self.response = self.client.get(reverse("homepage"))

    def test_unauth_access_homepage(self):
        """Prove that an unauth user can access the home page."""
        self.assertEqual(self.response.status_code, 200)

    def test_home_page_uses_right_template(self):
        """Assert that the home page is rendered with right template."""
        for template_name in [
            'securedpi/home_page.html', 'securedpi/base.html'
        ]:
            self.assertTemplateUsed(self.response, template_name)


class RegistrationTestCase(TestCase):
    """Setup Registration test case."""
    def setUp(self):
        """Set up for registration test case."""
        self.url = reverse('registration_register')
        self.get_response = self.client.get(self.url)
        self.post_response = self.client.post(
            self.url,
            {
                'username': 'user1',
                'email': 'user1@gmail.com',
                'password1': 'user1passwordsecret',
                'password2': 'user1passwordsecret'
            })

    def test_access_for_unauth_users_ok(self):
        """Prove that unauth users can access the registration page."""
        self.assertEqual(self.get_response.status_code, 200)

    def test_registration_page_uses_right_template(self):
        """Assert that registration page is rendered with right template."""
        template_name = 'registration/registration_form.html'
        self.assertTemplateUsed(self.get_response, template_name)

    def test_redirect_after_registred(self):
        """Test redirection from the page on successful registration."""
        self.assertEqual(self.post_response.status_code, 302)

    def test_correct_url_on_redirect_after_registred(self):
        """Test redirecte url upon successful registration."""
        self.assertEqual(
            self.post_response.url,
            reverse('registration_complete'))
