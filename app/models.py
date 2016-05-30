import datetime

import flask.ext.whooshalchemy as whooshalchemy
from flask.ext.security import SQLAlchemyUserDatastore, UserMixin, RoleMixin

from app import app, db

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(45))
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Operations(db.Model):
    __tablename__ = 'operations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    operation = db.Column(db.String(200))
    timestamp = db.Column(db.TIMESTAMP)


class Rates(db.Model):
    __tablename__ = 'rates'
    __searchable__ = ['date', 'client', 'rate', 'origin', 'destination', 'type', 'terms', 'manager', 'comments']
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    client = db.Column(db.String(100))
    rate = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    capacity = db.Column(db.String(100))
    type = db.Column(db.String(100))
    terms = db.Column(db.String(500))
    manager = db.Column(db.String(100))
    comments = db.Column(db.String(500))
    created_by = db.Column(db.Integer)
    is_new = db.Column(db.Boolean)
    taken_by = db.Column(db.Integer)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
whooshalchemy.whoosh_index(app, Rates)
