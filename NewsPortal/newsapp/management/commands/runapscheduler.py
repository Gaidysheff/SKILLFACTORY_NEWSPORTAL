from django.conf import settings
from newsapp.models import Post, Category, Subscribe

import logging
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


logger = logging.getLogger(__name__)


def my_job():
    # ============================ Mailing to subscribers for all news =======================
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    subscribers_for_all = set(
        Subscribe.objects.all().values_list('email', flat=True))

    mailing_list_for_all = ''
    for el in subscribers_for_all:
        mailing_list_for_all += str(el)
        mailing_list_for_all += ', '

    html_content = render_to_string(
        'newsapp/mail_weekly.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        },
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.DEFAULT_TO_EMAIL, mailing_list_for_all]
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

    # ============================ Mailing to subscribers on Categories =======================

    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(Category.objects.filter(
        name__in=categories).values_list('categorysubscribe__subscriber', flat=True))

    mailing_list = ''
    for el in subscribers:
        mailing_list += str(el)
        mailing_list += ', '

    html_content = render_to_string(
        'newsapp/mail_weekly_category.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
            'categories': categories,
            # 'Link': f'{settings.SITE_URL}/post/<slug:post_slug>/'
        },
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.DEFAULT_TO_EMAIL, mailing_list]
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/30"),
            # trigger=CronTrigger(day_of_week="mon", hour='00', minute='00'),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
