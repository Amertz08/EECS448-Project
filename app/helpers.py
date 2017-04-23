from __future__ import unicode_literals, print_function, division, absolute_import

import datetime
import traceback

from flask import current_app

from mail import send_email


def send_error_email():
    """
    Catches exception and emails application administrator
    :return: None 
    """
    error = traceback.format_exc()

    send_email(
        recipients=[current_app.config['ADMIN_EMAIL']],
        subject='[{}] Application Error'.format(current_app.config['CONFIG_LVL']),
        template_name='error',
        context={
            'error': error,
            'time': datetime.datetime.now()
        }
    )
