from __future__ import absolute_import, unicode_literals
# from celery.schedules import crontab

from celery.utils.log import get_task_logger

from celery import shared_task

# from .email import send_postCreation_email
from .email import send_subscribe_email, send_subscribe_category_email

from .email import send_postCreation_email

logger = get_task_logger(__name__)

# @task(name='send_postCreation_email_task')
# def send_postCreation_email_task(email):
#     logger.info('Info email to subscriber has been sent')
#     return send_postCreation_email(email)

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


# @shared_task
# def add(x, y):
#     return x + y

