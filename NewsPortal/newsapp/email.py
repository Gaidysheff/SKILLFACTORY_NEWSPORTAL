from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from NewsPortal.settings import DEFAULT_FROM_EMAIL

# def send_postCreation_email(email):

#     context = {
#         'email': email
#     }

#     email_subject = "Опубликована новая статья"
#     email_body = render_to_string('emal_message.txt', context)

#     email = EmailMessage(
#         email_subject, email_body,
#         settings.DEFAULT_FROM_EMAIL, [email, ],
#     )
#     return email.send(fail_silently=False)

def send_subscribe_email(email):

    context = {
        'email': email,
    }

    email_subject = "Подписка на рассылку новостей"
    email_body = render_to_string('emal_message.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return email.send(fail_silently=False)


