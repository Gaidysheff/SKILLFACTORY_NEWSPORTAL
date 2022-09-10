from ast import arg
from django.forms import EmailInput, CharField
from django.utils.translation import gettext_lazy as _
from distutils.text_file import TextFile
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
        fields = ('username', 'email', 'password1', 'password2', )


class LoginFormUser(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-control'})),
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput(
        attrs={'class': 'form-control'})),


class SubscribeForm(forms.ModelForm):
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'size': 30,
            'placeholder': "Your email ...",
        }))

    class Meta:
        model = Subscribe
        fields = ('email', )


class CategorySubscribeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categorySubscribed'].empty_label = 'Категория не выбрана'

    class Meta:
        model = CategorySubscribe
        fields = ('subscriber', 'categorySubscribed')
        # widgets = {'subscriber': EmailInput(attrs={'class': 'form-input', 'size': 30, 'placeholder': 'Your email ...'}),
        #            'categorySubscribed': CharField(attrs={'class': 'form-input', 'size': 30, 'placeholder': 'Your email ...'}),
        #            }
        labels = {'subscriber': _('Your email :'), 'categorySubscribed': _(
            'Категория для подписки :'), }
        help_texts = {'subscriber': _('Please, enter your E-mail'), }
        error_messages = {'subscriber': {
            'max_length': _('This is not correct E-mail'), }, }


# class CategorySubscribeForm(forms.Form):
#     subscriber = forms.EmailField(
#         label='E-mail',
#         widget=forms.EmailInput(
#             attrs={'class': 'form-input', 'size': 30, 'placeholder': "Your email ...", })
#     )
#     categorySubscribed = forms.CharField(
#         label='Категория', widget=forms.TextInput(attrs={'class': 'form-input'}))


"""  https://metanit.com/python/django/4.1.php  """


class NewSubForm(forms.ModelForm):
    subscriber = forms.EmailField(label='E-mail')
    categorySubscribed = forms.CharField(label='Категория')

    class Meta:
        model = CategorySubscribe
        fields = ['subscriber', 'categorySubscribed']
