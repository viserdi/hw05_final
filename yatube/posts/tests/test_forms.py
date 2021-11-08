import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..forms import PostForm
from ..models import Group, Post, User
from .test_const import (CREATE_URL, FORM_GROUP_DESCRIPTION, FORM_GROUP_SLUG,
                         FORM_GROUP_TITLE, FORM_POST_TEXT, PROFILE2_URL,
                         USERNAME2)

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USERNAME2)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title=FORM_GROUP_TITLE,
            slug=FORM_GROUP_SLUG,
            description=FORM_GROUP_DESCRIPTION
        )
        cls.post = Post.objects.create(
            text=FORM_POST_TEXT,
            author=cls.user,
            group=cls.group
        )
        cls.form = PostForm()
        cls.EDIT_URL = reverse(
            'posts:post_edit', kwargs={'post_id': cls.post.id}
        )
        cls.DETAIL_URL = reverse(
            'posts:post_detail', kwargs={'post_id': cls.post.id}
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_create_post_form_with_pic(self):
        """Проверка появления новой записи с картинкой в БД"""
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': FORM_POST_TEXT,
            'image': uploaded,
        }
        response = self.authorized_client.post(
            CREATE_URL,
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            PROFILE2_URL,
            msg_prefix='Редирект работает неверно'
        )
        self.assertEqual(
            Post.objects.count(),
            posts_count + 1,
            'Новый пост не появился'
        )
        self.assertTrue(
            Post.objects.filter(
                text=FORM_POST_TEXT,
                image='posts/small.gif',
            ).exists()
        )

    def test_edit_post_form(self):
        """Проверка изменения записи в БД"""
        old_text = self.post.text
        form_data_new = {
            'text': 'Новый текст'
        }
        response = self.authorized_client.post(
            self.EDIT_URL,
            data=form_data_new,
            follow=True
        )
        new_text = Post.objects.all().last().text
        self.assertNotEqual(
            new_text,
            old_text,
            'Текст поста не изменился'
        )
        self.assertRedirects(
            response,
            self.DETAIL_URL,
            msg_prefix='Редирект работает неверно'
        )
