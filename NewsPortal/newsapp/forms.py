from django.contrib.auth.forms import AuthenticationForm
from turtle import width
from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = 'Автор не выбран'
        self.fields['postCategory'].empty_label = 'Категория не выбрана'
        self.fields['postCategory'].widget.attrs.update(
            {'class': 'btn btn-secondary dropdown-toggle'}, size='7')
        self.fields['author'].widget.attrs.update(
            {'class': 'btn btn-secondary dropdown-toggle', 'type': 'button', 'data-toggle': 'dropdown', 'aria-haspopup': 'true', 'aria-expanded': 'false'})
        self.fields['categoryType'].widget.attrs.update(
            {'class': 'btn btn-secondary dropdown-toggle'})
        self.fields['status'].widget.attrs.update(
            {'class': 'btn btn-secondary dropdown-toggle'})

    class Meta:
        model = Post
        fields = ['author', 'categoryType', 'postCategory',
                  'title', 'slug', 'text', 'photo', 'rating', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'size': 58}),
            'slug': forms.URLInput(attrs={'size': 58}),
            'text': forms.Textarea(attrs={'cols': 60, 'rows': 7}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')
        return title


class SignUpUserForm(UserCreationForm):
    username = forms.CharField(
        label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'})),
    email = forms.EmailField(
        label='e-mail', widget=forms.EmailInput(attrs={'class': 'form-control'})),
    password1 = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'})),
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(
        attrs={'class': 'form-control'})),

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginFormUser(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-control'})),
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput(
        attrs={'class': 'form-control'})),
