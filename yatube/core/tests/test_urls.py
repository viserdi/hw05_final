from django.test import Client, TestCase

from .test_const import CORE_URL_404


class CoreURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_core_urls_uses_correct_template(self):
        """URL-адрес core использует соответствующий шаблон."""
        templates_url_names = {
            CORE_URL_404: 'core/404.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertTemplateUsed(response, template)
