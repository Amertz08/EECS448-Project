from __future__ import unicode_literals, print_function, division, absolute_import

from flask_mail import Message

from create import mail, celery


@celery.task
def send_async_email(**kwargs):
    msg = Message(**kwargs)
    mail.send(msg)
