from __future__ import unicode_literals, print_function, absolute_import
import os

from flask_script import Manager

from app.create import create_app

application = create_app(os.getenv('APP_CONFIG') or 'default')

manager = Manager(application)

if __name__ == '__main__':
    manager.run()
