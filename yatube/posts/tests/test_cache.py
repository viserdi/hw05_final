from django.core.cache import cache
from django.test import Client, TestCase

from ..models import Post, User
from .test_const import CACHE_POST_TEXT, INDEX_URL, USERNAME1


class PostViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username=USERNAME1)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.post = Post.objects.create(
            text=CACHE_POST_TEXT,
            author=cls.user,
        )

    def test_cache_index(self):
        """Проверка работы кэша на главной странице."""
        response = self.authorized_client.get(INDEX_URL)
        self.post.delete()
        response2 = self.authorized_client.get(INDEX_URL)
        self.assertEqual(
            response.content,
            response2.content,
            'Кэш главной страницы работает не верно',
        )
        cache.clear()
        response3 = self.authorized_client.get(INDEX_URL)
        self.assertNotEqual(
            response.content,
            response3.content,
            'Кэш не очистился или работает неверно'
        )
