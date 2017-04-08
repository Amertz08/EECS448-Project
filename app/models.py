from __future__ import unicode_literals, print_function, division, absolute_import

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import exc as sqlalchemy_exc


db = SQLAlchemy()


def commit(session):
    try:
        # If commit is True, commit the transaction
        session.commit()
    except sqlalchemy_exc.SQLAlchemyError as commit_exc:
        try:
            session.rollback()
        except sqlalchemy_exc.SQLAlchemyError as rollback_exc:
            # If rollback fails, log the exception
            pass
        raise commit_exc


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), default='')
    last_name = db.Column(db.String(255), default='')
    password = db.Column(db.String(255))
    city = db.Column(db.String(32), default='')
    state = db.Column(db.String(2), default='')
    zip_code = db.Column(db.Integer)
    email = db.Column(db.String(255), unique=True, default='')

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.hash_password(password)

    def __repr__(self):
        return '<User {first} {last} {email}>'.format(
            first=self.first_name,
            last=self.last_name,
            email=self.email
        )

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
