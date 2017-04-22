from __future__ import unicode_literals, print_function, division, absolute_import

import os
from create import create_app, celery

app = create_app(os.getenv('APP_CONFIG') or 'default')

app.app_context().push()
