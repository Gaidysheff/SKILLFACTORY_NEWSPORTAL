from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post, Subscribe, Category


@receiver(post_save, sender=Post)
def notify_post(sender, instance, created, **kwargs):
    if created:
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
                # 'Link': f'{settings.SITE_URL_SEND}/post/<slug:post_slug>/'
            },
        )

        # _post = Post.objects.all()
        # post = _post[len(_post)-1]
        post = Post.objects.last()

        msg = EmailMultiAlternatives(
            subject=f'Новая статья от автора { post.author }',
            from_email='gaidysheff@yandex.ru',
            to=['gaidysheff@mail.ru', mailing_list]
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()


@receiver(m2m_changed, sender=Category)
def notify_post_in_category(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        category = instance.category.all()
        subscribers_emails = []

        for cat in category:
            subscribers_in_category = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers_in_category]

        html = render_to_string(
            'newsapp/mail_category.html',
            {
                'user': subscribers_in_category,
                'post': instance,
                # 'Link': f'{settings.SITE_URL_SEND}/category/<slug:postCategory_slug>/'
            },
        )

        _post = Post.objects.all()
        post = _post[len(_post)-1]

        msg = EmailMultiAlternatives(
            subject=f'Новая статья от автора { post.author }',
            from_email='gaidysheff@yandex.ru',
            to=['gaidysheff@mail.ru', subscribers_in_category]
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()
