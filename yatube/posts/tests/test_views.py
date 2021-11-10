import shutil
import tempfile

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Comment, Follow, Group, Post, User
from .test_const import (COMMENT_TEXT, CREATE_URL, FOLLOW_POST_TEXT,
                         FOLLOW_URL, GROUP1_URL, GROUP2_DESCRIPTION,
                         GROUP2_SLUG, GROUP2_TITLE, GROUP2_URL,
                         GROUP_DESCRIPTION, GROUP_SLUG, GROUP_TITLE, INDEX_URL,
                         POST_TEXT, PROFILE_URL, SMALL_GIF, USERNAME1,
                         USERNAME2, USERNAME3)

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username=USERNAME1)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.user2 = User.objects.create_user(username=USERNAME2)
        cls.authorized_client2 = Client()
        cls.authorized_client2.force_login(cls.user2)
        cls.user3 = User.objects.create_user(username=USERNAME3)
        cls.authorized_client3 = Client()
        cls.authorized_client3.force_login(cls.user3)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESCRIPTION
        )
        cls.group2 = Group.objects.create(
            title=GROUP2_TITLE,
            slug=GROUP2_SLUG,
            description=GROUP2_DESCRIPTION
        )
        posts = []
        for i in range(13):
            posts.append(
                Post(
                    text=f'Тестовый пост{i}',
                    author=cls.user,
                    group=cls.group
                )
            )
        Post.objects.bulk_create(posts)
        Post.objects.create(
            text='Тестовый пост13',
            author=cls.user2,
            group=cls.group2
        )
        cls.post_list = list(Post.objects.all())
        cls.post2 = cls.post_list[0]
        cls.post = cls.post_list[1]
        cls.EDIT_URL = reverse(
            'posts:post_edit', kwargs={'post_id': cls.post.id}
        )
        cls.DETAIL_URL = reverse(
            'posts:post_detail', kwargs={'post_id': cls.post.id}
        )
        cls.TO_FOLLOW = reverse(
            'posts:profile_follow',
            kwargs={'username': USERNAME1}
        )
        cls.TO_FOLLOW2 = reverse(
            'posts:profile_follow',
            kwargs={'username': USERNAME2}
        )
        cls.TO_UNFOLLOW2 = reverse(
            'posts:profile_unfollow',
            kwargs={'username': USERNAME2}
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            INDEX_URL: 'posts/index.html',
            GROUP1_URL: 'posts/group_list.html',
            PROFILE_URL: 'posts/profile.html',
            self.DETAIL_URL: 'posts/post_detail.html',
            CREATE_URL: 'posts/create_post.html',
            self.EDIT_URL: 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_first_page_contains_ten_records(self):
        """Проверка паджинатора на первой странице (10 постов)."""
        pages = [
            INDEX_URL,
            PROFILE_URL,
            GROUP1_URL,
        ]
        for page in pages:
            response = self.authorized_client.get(page)
            self.assertEqual(
                len(response.context['page_obj']),
                10,
                'Проверьте работу паджинатора'
            )

    def test_second_page_contains_three_records(self):
        """Проверка паджинатора на второй странице."""
        pages = [
            INDEX_URL,
            PROFILE_URL,
            GROUP1_URL,
        ]
        for page in pages:
            if page == reverse('posts:index'):
                count = 4
            else:
                count = 3
            response = self.authorized_client.get(page + '?page=2')
            self.assertEqual(
                len(response.context['page_obj']),
                count,
                'Проверьте работу паджинатора'
            )

    def test_index_context(self):
        """Проверка правильной передачи контекста на главную страницу."""
        cache.clear()
        response = self.guest_client.get(INDEX_URL)
        self.assertEqual(
            response.context.get('page_obj').object_list[:3],
            self.post_list[:3],
            'Неправильный вывод постов на главную страницу'
        )

    def test_group_list_context(self):
        """Проверка правильного отображения постов на странице группы."""
        cache.clear()
        self.post_list = self.post_list[1::]
        response = self.guest_client.get(
            GROUP1_URL,
            headers={'Cache-Control': 'no-cache'}
        )
        self.assertEqual(
            response.context.get('page_obj').object_list[:3],
            self.post_list[:3],
            'Неправильный вывод постов на страницу группы'
        )
        for i in range(10):
            self.assertEqual(
                response.context.get('page_obj').object_list[i].group.title,
                self.group.title,
                'Посты не отфильтрованы по группе'
            )
        self.assertEqual(
            response.context.get('group').title,
            self.group.title,
            'Не верно передана группа в context'
        )

    def test_profile_context(self):
        """Проверка правильного отображения постов на странице профиля."""
        cache.clear()
        self.post_list = self.post_list[1::]
        response = self.guest_client.get(
            PROFILE_URL,
            headers={'Cache-Control': 'no-cache'}
        )
        self.assertEqual(
            response.context.get('page_obj').object_list[:3],
            self.post_list[:3],
            'Неправильный вывод постов на страницу профиля'
        )
        for i in range(10):
            post = response.context.get('page_obj').object_list[i]
            self.assertEqual(
                post.author.username,
                self.user.username,
                'Посты не отфильтрованы по автору'
            )

    def test_post_detail_context(self):
        """Проверка контекста, передаваемого в post_detail."""
        response = self.guest_client.get(self.DETAIL_URL)
        self.assertEqual(
            response.context['post'].id,
            self.post.id,
            'Неверный вывод поста в post_detail'
        )
        self.assertEqual(
            response.context['title'],
            self.post.text[:30],
            'Неверно передан title в post_detail'
        )

    def test_post_edit_form(self):
        """Проверка формы редактирования поста."""
        response = self.authorized_client.get(self.EDIT_URL)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(
                    form_field,
                    expected,
                    'Поля формы заданы неверно'
                )
        self.assertEqual(
            response.context.get('post_id'),
            self.post.id,
            'Неверно передан post_id'
        )

    def test_create_post_form(self):
        """Проверка формы создания поста."""
        response = self.authorized_client.get(CREATE_URL)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(
                    form_field,
                    expected,
                    'Поля формы заданы неверно'
                )

    def test_new_post_on_different_pages(self):
        """Отображение нового поста на разных страницах
        метод: проверка количества записей До и После.
        """
        Post.objects.create(
            text='Тестовый пост14',
            author=self.user,
            group=self.group
        )
        pages = {
            'index': [
                INDEX_URL,
                INDEX_URL + '?page=2'
            ],
            'group': [
                GROUP1_URL,
                GROUP1_URL + '?page=2'
            ],
            'profile': [
                PROFILE_URL,
                PROFILE_URL + '?page=2'
            ]
        }
        posts_count = {
            'index': 0,
            'group': 0,
            'profile': 0,
        }
        for name, page in pages.items():
            if name == 'index':
                before_posts_count = len(self.post_list)
            else:
                before_posts_count = len(self.post_list) - 1
            for i in range(2):
                response = self.guest_client.get(page[i])
                posts_count[name] += len(
                    response.context.get('page_obj').object_list
                )
            self.assertEqual(
                posts_count[name],
                before_posts_count + 1,
                f'На странице {name} не появился новый пост'
            )
        response = self.guest_client.get(GROUP2_URL)
        before_posts_count = 1
        other_pages = {
            'group': [
                GROUP2_URL,
                GROUP2_URL + '?page=2'
            ],
        }
        for name, page in other_pages.items():
            for i in range(2):
                response = self.guest_client.get(page[i])
                posts_count[name] += len(
                    response.context.get('page_obj').object_list
                )
            self.assertNotEqual(
                posts_count[name],
                before_posts_count + 1,
                f'Новый пост не принадлежит группе {self.group2.title}'
            )
        Post.objects.filter(id=14).delete()

    def test_new_post_on_different_pages_ver2(self):
        """Отображение нового поста на разных страницах вариант 2.
        Метод: поиск нового поста на странице index, group_list, profile.
        """
        new_post = Post.objects.create(
            text='Тестовый пост15',
            author=self.user,
            group=self.group
        )
        pages = {
            'index': INDEX_URL,
            'group': GROUP1_URL,
            'profile': PROFILE_URL,
        }
        for name, template in pages.items():
            with self.subTest(reverse_name=template):
                response = self.guest_client.get(template)
                self.assertEqual(
                    response.context.get('page_obj').object_list[0],
                    new_post,
                    f'Нет нового поста на странице {name}'
                )

    def test_new_comment(self):
        """Проверка появления нового комментария на странице."""
        count_of_comments = Comment.objects.filter(post=self.post).count()
        Comment.objects.create(
            post=self.post,
            text=COMMENT_TEXT,
            author=self.user
        )
        response = self.guest_client.get(self.DETAIL_URL)
        self.assertEqual(
            response.context['comments'].count(),
            count_of_comments + 1,
            'На странице поста не появился новый комментарий'
        )

    def test_new_post_with_pic_on_different_pages(self):
        """Проверка передачи картинки через context на разные страницы."""
        cache.clear()
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=SMALL_GIF,
            content_type='image/gif'
        )
        new_post = Post.objects.create(
            text='Тестовый пост с картинкой',
            author=self.user,
            group=self.group,
            image=uploaded
        )
        pages = {
            'index': INDEX_URL,
            'group': GROUP1_URL,
            'profile': PROFILE_URL,
        }
        for name, template in pages.items():
            with self.subTest(reverse_name=template):
                response = self.guest_client.get(template)
                self.assertTrue(
                    response.context.get('page_obj').object_list[0].image,
                    f'Нет картинки поста на странице {name}'
                )
        response = self.guest_client.get(
            reverse(
                'posts:post_detail', kwargs={'post_id': new_post.id}
            )
        )
        self.assertTrue(
            response.context['post'].image,
            'Не появилась картинка на странице поста'
        )

    def test_follow_unfollow_autorized(self):
        """Проверка, что авторизованный пользователь может подписаться
        и удалять из подписок авторов.
        """
        follow_count = Follow.objects.filter(user=self.user).count()
        self.authorized_client.get(self.TO_FOLLOW2)
        new_follow_count = Follow.objects.filter(user=self.user).count()
        self.assertEqual(
            new_follow_count,
            follow_count + 1,
            'У пользователя не появляется новая подписка',
        )
        self.authorized_client.get(self.TO_UNFOLLOW2)
        delete_follow_count = Follow.objects.filter(user=self.user).count()
        self.assertEqual(
            delete_follow_count,
            new_follow_count - 1,
            'Пользователь не может отписаться от автора'
        )

    def test_new_post_only_for_followers(self):
        """Проверка, что запись появляется у подписчика и не появляется
        у пользователя, который не подписан на автора.
        """
        Follow.objects.create(
            user=self.user,
            author=self.user3
        )
        Follow.objects.create(
            user=self.user2,
            author=self.user
        )
        new_follow_post = Post.objects.create(
            text=FOLLOW_POST_TEXT,
            author=self.user3,
        )
        Post.objects.create(
            text=POST_TEXT,
            author=self.user2,
        )
        response1 = self.authorized_client.get(FOLLOW_URL)
        response2 = self.authorized_client2.get(FOLLOW_URL)
        self.assertEqual(
            response1.context.get('page_obj').object_list[0],
            new_follow_post,
            'у подписчика не появился новый пост в ленте'
        )
        self.assertNotEqual(
            response2.context.get('page_obj').object_list[0],
            new_follow_post,
            'Пост появился у неподписанного на автора пользователя'
        )

    def test_follow_user_is_author(self):
        """Проверка, что пользователь не может подписаться сам на себя."""
        count_of_follows = Follow.objects.filter(user=self.user).count()
        self.authorized_client.get(self.TO_FOLLOW)
        new_count = Follow.objects.filter(user=self.user).count()
        self.assertEqual(
            count_of_follows,
            new_count,
            'Пользователь не может подписаться сам на себя'
        )

    def test_follow_only_once(self):
        """Проверка, что на автора можно подписаться лишь раз."""
        for i in range(2):
            self.authorized_client.get(self.TO_FOLLOW2)
        count = Follow.objects.filter(user=self.user).count()
        self.assertEqual(
            count,
            1,
            'Нельзя подписываться на автора несколько раз'
        )
