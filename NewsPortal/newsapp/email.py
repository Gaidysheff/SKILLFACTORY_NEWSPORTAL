from datetime import datetime, timedelta

from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from NewsPortal.settings import DEFAULT_FROM_EMAIL

from .models import CategorySubscribe, Post


def send_subscribe_email(email):

    context = {
        'email': email,
    }

    email_subject = "Подписка на рассылку новостей"
    email_body = render_to_string('emal_message_subscribe_all.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return email.send(fail_silently=False)


def send_subscribe_category_email(email):

    context = {
        'email': email,
        # 'categorySubscribed': categorySubscribed,
    }

    email_subject = "Подписка на рассылку новостей  в выбранной категории"
    email_body = render_to_string('emal_message_subscribe_category.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return email.send(fail_silently=False)


def send_postCreation_email(email, title, text):

    context = {
        'email': email,
        'title': title,
        'text': text,
    }

    email_subject = "Опубликована новая статья"
    email_body = render_to_string('emal_message_postCreation.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return email.send(fail_silently=False)

