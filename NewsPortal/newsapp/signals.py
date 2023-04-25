from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings

from .models import Post, Subscribe, Category, CategorySubscribe


@receiver(post_save, sender=Post)
def notify_post(sender, instance, created, **kwargs):
    if created:
        post = Post.objects.last()
        # _post = Post.objects.all()
        # post = _post[len(_post)-1]
        slug = post.slug
        subscribers = list(Subscribe.objects.values_list('email', flat=True))
        mailing_list = ''
        for el in subscribers:
            mailing_list += str(el)
            mailing_list += ', '
        html = render_to_string(
            'newsapp/mail.html',
            {
                'user': mailing_list,
                'post': instance,
                # 'Link': f'{settings.SITE_URL}/post/{slug}'
            },
        )

        msg = EmailMultiAlternatives(
            subject=f'Новая статья от автора { post.author }',
            from_email='gaidysheff@yandex.ru',
            to=['gaidysheff@mail.ru', mailing_list]
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()


# ==================== to Category subscribers ==================================
# @receiver(m2m_changed, sender=Category)
# def notify_post_in_category(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
@receiver(post_save, sender=Post)
def notify_post(sender, instance, created, **kwargs):
    if created:
        post = Post.objects.last()
        slug = post.slug
        category = post.postCategory
        cat_subscribers = set(Category.objects.filter(name=category).values_list(
            'categorysubscribe__subscriber', flat=True))

        users_list = ''
        for el in cat_subscribers:
            users_list += str(el)
            users_list += ', '

            html = render_to_string(
                'newsapp/mail_category.html',
                {
                    'user': users_list,
                    'post': instance,
                    # 'Link': f'{settings.SITE_URL}/post/{slug}'
                },
            )

    #         _post = Post.objects.all()
    #         post = _post[len(_post)-1]

            msg = EmailMultiAlternatives(
                subject=f'Новая статья от автора { post.author }',
                from_email='gaidysheff@yandex.ru',
                to=['gaidysheff@mail.ru', users_list]
            )

            msg.attach_alternative(html, 'text/html')
            msg.send()
