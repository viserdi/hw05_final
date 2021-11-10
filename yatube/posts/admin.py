from django.conf import settings as s
from django.contrib import admin

from .models import Comment, Follow, Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = s.IT_IS_EMPTY


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    search_fields = ('title',)
    empty_value_display = s.IT_IS_EMPTY


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text', 'created')
    search_fields = ('text',)
    list_filter = ('created',)
    empty_value_display = s.IT_IS_EMPTY


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author', )
    empty_value_display = s.IT_IS_EMPTY
