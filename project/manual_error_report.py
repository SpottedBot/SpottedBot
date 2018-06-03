import sys
from django.core import mail
from django.views.debug import ExceptionReporter
from celery import shared_task


@shared_task
def celery_admin_mail(subject, message, html):
    mail.mail_admins(
        subject, message, fail_silently=True,
        html_message=html
    )


def exception_email(request, e):
    exc_info = sys.exc_info()
    reporter = ExceptionReporter(request, is_email=True, *exc_info)
    try:
        subject = e.message.replace('\n', '\\n').replace('\r', '\\r')[:989]
    except AttributeError:
        subject = "Unkown Error"
    message = reporter.get_traceback_text()
    celery_admin_mail.delay(subject, message, reporter.get_traceback_html())


def no_request_exception(tb, e):
    try:
        subject = e.message.replace('\n', '\\n').replace('\r', '\\r')[:989]
    except AttributeError:
        subject = "Unkown Error"
    message = tb
    celery_admin_mail.delay(subject, message, tb)
