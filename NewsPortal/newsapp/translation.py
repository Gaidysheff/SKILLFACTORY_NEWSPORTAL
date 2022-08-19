from .models import Category, Post
from modeltranslation.translator import register, TranslationOptions


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    # указываем, какие именно поля надо переводить в виде кортежа
    fields = ('name', )


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text', )
