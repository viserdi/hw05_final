from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        help_texts = {
            'text': 'Тест поста',
            'group': 'Группа, к которой относится пост',
            'image': 'Картинка для поста'
        }

    def clean_text(self):
        data = self.cleaned_data.get('text')
        if not data:
            raise forms.ValidationError('Поле поста не должно быть пустым')
        return data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        help_texts = {
            'text': 'Текст Вашего комментария',
        }

    def clean_text(self):
        data = self.cleaned_data.get('text')
        if not data:
            raise forms.ValidationError('Поле поста не должно быть пустым')
        return data
