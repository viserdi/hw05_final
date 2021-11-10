from django.test import TestCase

from ..models import Comment, Follow, Group, Post, User
from .test_const import (COMMENT_TEXT, GROUP_DESCRIPTION, GROUP_SLUG,
                         GROUP_TITLE, MODEL_AUTHOR, MODEL_POST_TEXT,
                         MODEL_USERNAME)


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=MODEL_USERNAME)
        cls.author = User.objects.create_user(username=MODEL_AUTHOR)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=MODEL_POST_TEXT,
        )
        cls.comment = Comment.objects.create(
            author=cls.user,
            post=cls.post,
            text=COMMENT_TEXT,
        )
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.author,
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        group = PostModelTest.group
        post = PostModelTest.post
        comment = PostModelTest.comment
        follow = PostModelTest.follow
        expected_objects_str = {
            group: group.title,
            post: post.text[:15],
            comment: comment.text[:15],
            follow: follow.user.username,
        }
        for name, expected in expected_objects_str.items():
            with self.subTest():
                self.assertEqual(
                    expected,
                    str(name),
                    f'Ошибка __str__ у {name}'
                )
