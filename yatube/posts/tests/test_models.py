from django.test import TestCase

from ..models import Group, Post, User
from .test_const import (GROUP_DESCRIPTION, GROUP_SLUG, GROUP_TITLE,
                         MODEL_POST_TEXT, MODEL_USERNAME)


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=MODEL_USERNAME)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=MODEL_POST_TEXT,
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

    def test_posts_have_correct_text(self):
        """Проверяем корректность текста поста __str___."""
        post = PostModelTest.post
        expected_object_text = post.text[:15]
        self.assertEqual(expected_object_text, str(post))
