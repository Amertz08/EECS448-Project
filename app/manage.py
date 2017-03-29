from __future__ import unicode_literals, print_function, division, absolute_import
import os

from flask_script import Manager, Shell
from flask_migrate import MigrateCommand
import pytest

from create import create_app
from models import db

application = create_app(os.getenv('APP_CONFIG') or 'default')


def make_shell_context():
    return dict(
        app=application, db=db
    )

manager = Manager(application)
manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))


@manager.command
def createdb():
    db.create_all()


@manager.command
def test():
    pytest.main()


if __name__ == '__main__':
    manager.run()
