from __future__ import unicode_literals, print_function, division, absolute_import

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), default='')
    last_name = db.Column(db.String(255), default='')
    email = db.Column(db.String(255), unique=True, default='')
