from __future__ import absolute_import, unicode_literals


from celery.utils.log import get_task_logger

from celery import shared_task
from .email import send_subscribe_email, send_subscribe_category_email, send_postCreation_email 
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
from NewsPortal.settings import DEFAULT_FROM_EMAIL

from .models import CategorySubscribe, Post

logger = get_task_logger(__name__)


@shared_task(name='send_subscribe_email_task')
def send_subscribe_email_task(email):
    logger.info('Confirmation email to subscriber has been sent')
    return send_subscribe_email(email,)

@shared_task(name='send_subscribe_category_email_task')
def send_subscribe_category_email_task(email):
    logger.info('Confirmation email to subscriber for category has been sent')
    return send_subscribe_category_email(email)

@shared_task(name='send_postCreation_email_task')
def send_postCreation_email_task(email, title, text):
    logger.info('Confirmation email that a new article has been created')
    return send_postCreation_email(email, title, text)


@shared_task
def send_weekly_notification_email():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers_list = ''
    for cat in categories:
        subscriber = list(CategorySubscribe.objects.filter(
            categorySubscribed__name=cat).values_list('subscriber', flat=True))
        subscribers_list += str(subscriber)
        subscribers_list += ', '
    
    html_content = render_to_string(
        'weekly_posts.html',
        {
            'subscribers_list': subscribers_list,
            'posts': posts, 
            'categories': categories, 
            'link': settings.SITE_URL,
            }
    )

    msg = EmailMultiAlternatives(
        subject='Публикации за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_list,
      
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()



