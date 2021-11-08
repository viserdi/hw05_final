from http import HTTPStatus

from django.test import Client, TestCase

from .urls_const import AUTHOR_URL, TECH_URL


class AboutURLsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_about_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            AUTHOR_URL: 'about/author.html',
            TECH_URL: 'about/tech.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_about_urls_avalible_for_all(self):
        """URL-адреса доступные для любого пользователя."""
        templates_url_names = [
            AUTHOR_URL,
            TECH_URL
        ]
        for adress in templates_url_names:
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)
