from __future__ import unicode_literals, print_function, division, absolute_import


from flask import current_app, render_template

from tasks import send_async_email


def send_email(recipients, subject, template_name, **context):
    with current_app.app_context():
        msg = {
            'sender': current_app.config['MAIL_DEFAULT_SENDER'],
            'subject': subject,
            'recipients': recipients,
            'body': render_template('emails/{}.txt'.format(template_name, **context)),
            'html': render_template('emails/{}.html'.format(template_name, **context))
        }
        send_async_email.delay(**msg)
