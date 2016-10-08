from django.test import TestCase
from django.urls import reverse


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
