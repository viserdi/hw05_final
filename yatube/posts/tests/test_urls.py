from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User
from .test_const import (CREATE_URL, GROUP1_URL, GROUP2_DESCRIPTION,
                         GROUP_SLUG, GROUP_TITLE, INDEX_URL, POST_TEXT,
                         PROFILE_URL, USERNAME1, USERNAME3)


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username=USERNAME1)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.user2 = User.objects.create_user(username=USERNAME3)
        cls.authorized_client2 = Client()
        cls.authorized_client2.force_login(cls.user2)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP2_DESCRIPTION
        )
        cls.post = Post.objects.create(
            text=POST_TEXT,
            author=cls.user,
            group=cls.group
        )
        cls.EDIT_URL = reverse(
            'posts:post_edit', kwargs={'post_id': cls.post.id}
        )
        cls.DETAIL_URL = reverse(
            'posts:post_detail', kwargs={'post_id': cls.post.id}
        )
        cls.COMMENT_URL = reverse(
            'posts:add_comment', kwargs={'post_id': cls.post.id}
        )
        cls.COMMENT_LOGIN = f'/auth/login/?next=/posts/{cls.post.id}/comment/'

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            INDEX_URL: 'posts/index.html',
            GROUP1_URL: 'posts/group_list.html',
            PROFILE_URL: 'posts/profile.html',
            self.DETAIL_URL: 'posts/post_detail.html',
            CREATE_URL: 'posts/create_post.html',
            self.EDIT_URL: 'posts/create_post.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_urls_avalible_for_all(self):
        """URL-адреса доступные для любого пользователя."""
        templates_url_names = [
            INDEX_URL,
            GROUP1_URL,
            PROFILE_URL,
            self.DETAIL_URL,
        ]
        for adress in templates_url_names:
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_edit_not_for_author(self):
        """Проверка перенаправления страницы для пользователя,
        не являющегося автором поста.
        """
        response = self.authorized_client2.get(self.EDIT_URL)
        self.assertRedirects(response, PROFILE_URL)

    def test_redirect_comment_for_guest(self):
        """Проверка, что неавторизованный пользователь
        не может комментировать пост.
        """
        response = self.guest_client.get(self.COMMENT_URL)
        self.assertRedirects(response, self.COMMENT_LOGIN)

    def test_status_code_create_edit_unexisting_for_different_users(self):
        """Проверка ответа страниц create, edit и несуществующей
        для пользователей с разным доступом
        """
        responses = {
            self.authorized_client.get(CREATE_URL): HTTPStatus.OK,
            self.guest_client.get(CREATE_URL): HTTPStatus.FOUND,
            self.authorized_client.get(self.EDIT_URL): HTTPStatus.OK,
            self.guest_client.get('unexisting_page/'): HTTPStatus.NOT_FOUND
        }
        for response, code in responses.items():
            with self.subTest():
                self.assertEqual(response.status_code, code)
