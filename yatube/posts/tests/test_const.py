from django.urls import reverse

INDEX_URL = reverse('posts:index')
FOLLOW_URL = reverse('posts:follow_index')
CREATE_URL = reverse('posts:post_create')
GROUP1_URL = reverse('posts:group_list', kwargs={'slug': 'test-slug'})
GROUP2_URL = reverse('posts:group_list', kwargs={'slug': 'test-slug2'})
GROUP3_URL = reverse('posts:group_list', kwargs={'slug': 'test-slug3'})
PROFILE_URL = reverse('posts:profile', kwargs={'username': 'TestName'})
PROFILE2_URL = reverse('posts:profile', kwargs={'username': 'TestName2'})

USERNAME1 = 'TestName'
USERNAME2 = 'TestName2'
USERNAME3 = 'NotAuthor'
GROUP_TITLE = 'Тестовая группа'
GROUP_SLUG = 'test-slug'
GROUP_DESCRIPTION = 'Тестовое описание'
GROUP2_TITLE = 'Тестовая группа 2'
GROUP2_SLUG = 'test-slug2'
GROUP2_DESCRIPTION = 'Тестовое описание 2'
POST_TEXT = 'Тестовый пост'

FORM_GROUP_TITLE = 'Тестовая группа для форм'
FORM_GROUP_SLUG = 'test-slug3'
FORM_GROUP_DESCRIPTION = 'Тестовое описание'
FORM_POST_TEXT = 'Тестовый пост для проверки форм'

MODEL_USERNAME = 'auth'
MODEL_AUTHOR = 'FollowMe'
MODEL_POST_TEXT = 'Тестовый текст модели'

COMMENT_TEXT = 'Тестовый комментарий'

CACHE_POST_TEXT = 'Тестовый пост для кэша'

FOLLOW_POST_TEXT = 'Тестовый текст для подписчика'

SMALL_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)

GARBAGE = 'garbage'
