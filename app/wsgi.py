from __future__ import unicode_literals, print_function, division, absolute_import

import os

from create import create_app

app = create_app(os.getenv('APP_CONFIG') or 'default')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
