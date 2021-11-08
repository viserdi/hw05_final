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
MODEL_POST_TEXT = 'Тестовый текст модели'

COMMENT_TEXT = 'Тестовый комментарий'

CACHE_POST_TEXT = 'Тестовый пост для кэша'

FOLLOW_POST_TEXT = 'Тестовый текст для подписчика'
