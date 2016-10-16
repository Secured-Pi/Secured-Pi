from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
from securedpi_locks.models import Lock


# class HomePageTestCase(TestCase):
#     """Create Home Page test case."""
#
#     def setUp(self):
#         """Set up response for home page test case."""
#         self.response = self.client.get(reverse("homepage"))

    # def test_unauth_access_about_page(self):
    #     """Prove that an unauth user can access About page."""
    #     response = self.client.get(reverse('about'))
    #     self.assertEqual(response.status_code, 200)


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
        template = 'registration/registration_form.html'
        self.assertTemplateUsed(self.get_response, template)

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


class LoginPageTestCase(TestCase):
    """Define clas  for login page testing."""
    def setUp(self):
        """Set up for testing."""
        self.url = reverse('auth_login')
        self.response = self.client.get(self.url)

    def test_access_for_unauth_users(self):
        """Make sure unauth users have access to Login page."""
        self.assertEqual(self.response.status_code, 200)

    def test_for_registration_button(self):
        """Prove login page contains registration page link."""
        reg_url = reverse("registration_register")
        expected = 'href="{}"'.format(reg_url)
        self.assertContains(self.response, expected)

    def test_fields_of_login_form(self):
        """Test that <username> and <password> fields are present."""
        username_filed = 'input type="text" name="username"'
        pass_field = 'input type="password" name="password"'
        login_button = "Login"
        expected = [username_filed, pass_field]
        for field in expected:
            self.assertContains(self.response, field)


class LoginLogoutTestCase(TestCase):
    """Define test case for Login/Logout functionality."""
    def setUp(self):
        """Set up response for login tests."""
        self.user = User(username='test')
        self.user.set_password('testpassword&#')
        self.user.save()
        self.dashboard_url = reverse('dashboard')
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

    def test_redirected_to_dashboard_after_logged_in(self):
        """Prove redirection to the home page after loggin in."""
        self.assertEqual(self.login_response.url, self.dashboard_url)

    def test_not_redirected_when_failed_login(self):
        """Prove that the user is not redirected if wrong credentials."""
        self.assertEqual(self.bad_login_response.status_code, 200)

    def test_logout_succesful_redirection(self):
        """Test successful logout redirection."""
        self.assertEqual(self.logout_response.status_code, 302)

    def test_redirected_to_dashboard_after_logged_out(self):
        """Prove redirection to the home page after loggin out."""
        self.assertEqual(self.logout_response.url, self.dashboard_url)


class DashboardViewTestCase(TestCase):
    """Define test class for Dashboard view."""
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
        self.url = reverse('dashboard')
        self.response = self.client.get(self.url)
        self.template = 'securedpi/dashboard.html'

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

    def test_username_displayed(self):
        """Make sure correct username is displayed."""
        self.assertContains(self.response, 'test')

    def test_expected_links_displayed(self):
        """Test thatexpected links and username are displayed."""
        urls = [
            'profile',
            'securedpi_facerec:train',
            'auth_logout',
        ]
        for url in urls:
            expected_link = 'href="{}"'.format(reverse(url))
            self.assertContains(self.response, expected_link)

    def test_lock_buttons_present(self):
        """Make sure each lock has <Edit> and <Access Log> buttons present."""
        lock_pks = [self.lock1.pk, self.lock2.pk]
        for lock_pk in lock_pks:
            edit_link = 'href="{}"'.format(reverse('edit_lock', kwargs={'pk': lock_pk}))
            log_link = 'href="{}"'.format(reverse('events', kwargs={'pk': lock_pk}))
            self.assertContains(self.response, edit_link)
            self.assertContains(self.response, log_link)

    def test_lock_info_present(self):
        """Make sure all lock have their info displayed."""
        locks = [self.lock1, self.lock2]
        for lock in locks:
            info = [
                lock.name,
                lock.pk,
                lock.serial,
                lock.location,
                lock.facial_recognition
                ]
            for item in info:
                self.assertContains(self.response, item)

    def test_buttons_display_if_unlocked(self):
        """
        Make sure <Lock> button shows up and <Unlock> doesn't
        if the lock.status == 'unlocked'."""
        self.lock1.status = 'unlocked'
        self.lock1.is_active = True
        self.lock1.save()
        response = self.client.get(self.url)
        self.assertContains(response, 'UNLOCKED')
        self.assertContains(response, self.expected1)
        self.assertNotContains(response, self.expected2)


    def test_buttons_display_if_locked(self):
        """
        Make sure <Unlock> button shows up and <Lock> doesn't
        if the lock.status == 'locked'."""
        self.lock1.status = 'locked'
        self.lock1.is_active = True
        self.lock1.save()
        response = self.client.get(self.url)
        self.assertContains(response, 'LOCKED')
        self.assertNotContains(response, self.expected1)
        self.assertContains(response, self.expected2)


    def test_buttons_display_if_pending(self):
        """
        Make sure both <Unlock> and <Lock> buttons show up
        if the lock.status == 'pending'."""
        self.lock1.status = 'pending'
        self.lock1.is_active = True
        self.lock1.save()
        response = self.client.get(self.url)
        self.assertContains(response, 'PENDING')
        self.assertContains(response, self.expected1)
        self.assertContains(response, self.expected2)


    def test_buttons_display_if_not_active(self):
        """
        Make sure <Unlock> and <Lock> buttons don't show up
        if the lock.is_active == False."""
        self.lock1.is_active = False
        self.lock1.save()
        response = self.client.get(self.url)
        self.assertContains(response, 'NOT ACTIVE')
        self.assertNotContains(response, self.expected1)
        self.assertNotContains(response, self.expected2)
