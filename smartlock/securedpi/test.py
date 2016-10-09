from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User


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

    def test_for_registration_button(self):
        """Prove home page contains registration page link."""
        reg_url = reverse("registration_register")
        expected = 'href="{}"'.format(reg_url)
        self.assertContains(self.response, expected, status_code=200)

    def test_for_login_button(self):
        """Assert that home page contains a link to the login page"""
        login_url = reverse('auth_login')
        expected = 'href="{}"'.format(login_url)
        self.assertContains(self.response, expected, status_code=200)


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


class EmailTest(TestCase):
    """Set up Email Test Class."""
    def test_send_email(self):
        """Tests that registration email was sent."""
        mail.send_mail(
            "Registration details", "This is the registration message.",
            'user@djangoimager.com', ['s@s.com', 'd@s.com'],
            fail_silently=False,
        )
        # Tests that an email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Verify the subject of the first message is as expected
        self.assertEqual(mail.outbox[0].subject, "Registration details")

        # Verify the message of the email is as expected
        self.assertEqual(
            mail.outbox[0].message()._payload,
            "This is the registration message.")

        # Verify the recipients are as expected
        self.assertEqual(mail.outbox[0].to, ['s@s.com', 'd@s.com'])

        # Verify the sender is as expected
        self.assertEqual(mail.outbox[0].from_email, "user@djangoimager.com")


class LoginLogoutTestCase(TestCase):
    """Define test case for Login/Logout functionality."""
    def setUp(self):
        """Set up response for login tests."""
        self.user = User(username='test')
        self.user.set_password('testpassword&#')
        self.user.save()
        self.home_url = reverse('homepage')
        self.login_url = reverse('auth_login')
        self.logout_url = reverse('auth_logout')
        self.bad_login_response = self.client.post(
            self.login_url,
            {"username": 'wrong', "password": "wrongpassword"}
        )
        self.login_response = self.client.post(
            self.login_url,
            {"username": 'test', "password": "testpassword&#"}
        )
        self.login_response_follow = self.client.post(
            self.login_url,
            {"username": 'test', "password": "testpassword&#"},
            follow=True
        )
        self.logout_response = self.client.get(self.logout_url)

    def test_redirection_after_logged_in(self):
        """Test successful login redirection."""
        self.assertEqual(self.login_response.status_code, 302)

    def test_redirected_to_homepage_after_logged_in(self):
        """Prove redirection to the home page after loggin in."""
        self.assertEqual(self.login_response.url, self.home_url)

    def test_not_redirected_when_failed_login(self):
        """Prove that the user is not redirected if wrong credentials."""
        self.assertEqual(self.bad_login_response.status_code, 200)

    def test_logout_succesful_redirection(self):
        """Test successful logout redirection."""
        self.assertEqual(self.logout_response.status_code, 302)

    def test_redirected_to_homepage_after_logged_out(self):
        """Prove redirection to the home page after loggin out."""
        self.assertEqual(self.logout_response.url, self.home_url)

    def test_welcome_username_linked_to_page(self):
        """Test that 'Welcome, <username>' links to expected page."""
        expected = 'href="{}"'.format(self.home_url)
        self.assertContains(self.login_response_follow, expected)

    def test_logout_button_exists(self):
        """Test auth user has logout button that links to correct url."""
        expected = 'href="{}"'.format(self.logout_url)
        self.assertContains(self.login_response_follow, expected)
