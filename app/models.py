from __future__ import unicode_literals, print_function, division, absolute_import

import datetime

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
    places = db.relationship('FavoritePlace')

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

    def update_password(self, password):
        self.password = self.hash_password(password)


class FavoritePlace(db.Model):
    __tablename__ = 'favorite_places'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    added = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    city = db.Column(db.String(32), default='')
    country = db.Column(db.String(32), default='')
    place_id = db.Column(db.String(32), default='')

    def __repr__(self):
        return '<FavoritePlace city: {0} country: {1} place_id: {2}>'.format(
            self.city, self.country, self.place_id
        )

    def __eq__(self, other):
        a = self.user_id == other.user_id
        b = self.place_id == other.place_id
        return a & b

    def __ne__(self, other):
        return self != other
