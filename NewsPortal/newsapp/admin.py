from django.contrib import admin


from django.contrib import messages
from django.utils.translation import ngettext

from .models import Author, Category, Comments, Post

from modeltranslation.admin import TranslationAdmin


# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/actions/

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    pass


class CommentsInline(admin.TabularInline):
    model = Comments
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'dateCreation', 'photo', 'categoryType', 'rating', 'status',
                    # 'display_category'
                    'категория', 'автор'
                    )
    list_display_links = ('id', 'title')
    search_fields = ('title', 'text')
    list_editable = ('categoryType', 'rating', 'status')
    list_filter = ('dateCreation', 'rating', 'postCategory')
    prepopulated_fields = {'slug': ('title',)}

    inlines = [CommentsInline]


# _______добавление команд в список действий в админке ____________

    actions = ['make_published', 'make_withdrawn']

    @admin.action(description='Опубликовать выбранные посты')
    def make_published(self, request, queryset):
        updated = queryset.update(status='p')
        self.message_user(request, ngettext(
            '%d публикация была отмечена как "Опубликованная".',
            '%d публикации были отмечены как "Опубликованные".',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Отправить выбранные посты в архив')
    def make_withdrawn(self, request, queryset):
        updated = queryset.update(status='w')
        self.message_user(request, ngettext(
            '%d публикация была отправлена в архив.',
            '%d публикации были отправлены в архив.',
            updated,
        ) % updated, messages.SUCCESS)

# -----------------------------------------------------------------

    @admin.display(ordering='author')
    def автор(self, obj):
        return obj.author

    @admin.display(ordering='-postCategory')
    def категория(self, obj):
        return obj.postCategory


class PostAdmin(TranslationAdmin):
    model = Post


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', )
    list_display_links = ('id', 'name')
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}

    class CategoryAdmin(TranslationAdmin):
        model = Category
