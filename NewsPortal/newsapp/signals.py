from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post, Subscribe


@receiver(post_save, sender=Post)
def notify_post(sender, instance, created, **kwargs):
    if created:
        user = list(Subscribe.objects.values_list('email', flat=True))
        mailing_list = ''
        for el in user:
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

        _post = Post.objects.all()
        post = _post[len(_post)-1]

        msg = EmailMultiAlternatives(
            subject=f'Новая статья от автора { post.author }',
            from_email='gaidysheff@yandex.ru',
            to=['gaidysheff@mail.ru', mailing_list]
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()
