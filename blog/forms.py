from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')
        labels = {'title': 'Заголовок', 'text': 'Текст', 'image': 'Загрузить изображение:'}
        widgets = {
            'title': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите название поста',
            'size': 30,
            }),
            'text': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Содержание поста',
            'rows': 3,
            'cols': 30,
            }),
            'image': forms.FileInput(attrs={
            'class': 'form-control',
            'id': 'my-image-upload',
            'accept': 'image/*',
            })
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author_name', 'text',)
        widgets = {
            'author_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя?',
            'size': 30,
            }),
            'text': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ваш комментарий',
            'rows': 3,
            'cols': 30,
            })
        }

