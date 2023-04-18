from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def update_rating(self):

        postRat = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentsRat = self.authorUser.comments_set.all(
        ).aggregate(commentsRating=Sum('rating'))
        cRat = 0
        cRat += commentsRat.get('commentsRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


# --------------------------------------------------------------------------------


class Post(models.Model):
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, verbose_name='Автор')

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    STATUS_CHOICES = [
        ('d', 'Черновик'),
        ('p', 'Опубликовано'),
        ('w', 'в архиве'),
    ]

    categoryType = models.CharField(
        max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE, verbose_name='Тип публикации')
    dateCreation = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    postCategory = models.ForeignKey(
        'Category', on_delete=models.CASCADE, verbose_name='Категория поста')
    title = models.CharField(max_length=128, verbose_name='Заголовок поста')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL', help_text=_('slug назначится автоматически'))
    text = models.TextField(null=True, blank=True, verbose_name=pgettext_lazy('for text in PostModel model', 'Текст поста (необязательно)'),
                            help_text=_('Введите здесь текст своего Поста, хотя можете и не вводить, если нет желания!'))
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d/", verbose_name='Изображение')
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг')
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default='d', verbose_name='Статус')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-dateCreation', 'title']

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return '{} ... {}'.format(self.text[0:123], str(self.rating))

    def save(self,  *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('post_detail', args=[str(self.id)])

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


# --------------------------------------------------------------------------------

    # def display_category(self):
    #     return '\n'.join([c.name for c in self.postCategory.all()])

    # display_category.short_description = 'Категория'

# --------------------------------------------------------------------------------


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')
    # subscriber = models.ManyToManyField(
    #     User, through='CategorySubscribe', blank=True, related_name='category')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'postCategory_slug': self.slug})
        # return reverse('category', kwargs={'cat_id': self.pk})

# --------------------------------------------------------------------------------


class Comments(models.Model):
    commentPost = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name='Заголовок поста')
    commentUser = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст поста',
                            help_text='Введите здесь текст своего комментария')
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг:')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text[:10]}...'

# --------Подписка по e-mail на все категории---------------------


class Subscribe(models.Model):
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


# # --------Подписка по e-mail на индивидуальную категорию----------

# class CategorySubscriber(models.Model):
#     subscriber_thru = models.ForeignKey(
#         User, on_delete=models.CASCADE, blank=True, null=True,)
#     category_thru = models.ForeignKey(
#         Category, on_delete=models.CASCADE, blank=True, null=True,)


class CategorySubscribe(models.Model):
    subscriber = models.EmailField()
    # subscriber = models.OneToOneField(User, on_delete=models.CASCADE)
    categorySubscribed = models.ManyToManyField(Category)

    def __str__(self):
        return self.subscriber
