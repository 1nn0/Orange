import flask.ext.whooshalchemy as whooshalchemy

from app import app, db

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(50))
    sname = db.Column(db.String(50))
    role = db.Column(db.Integer, default=ROLE_USER)
    last_login = db.Column(db.DATETIME)
    rates_taken = db.relationship('Rates', backref='logist', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.login)


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
    date = db.Column(db.String(100))
    client = db.Column(db.String(100))
    rate = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    capacity = db.Column(db.String(100))
    type = db.Column(db.String(100))
    terms = db.Column(db.String(500))
    manager = db.Column(db.String(100))
    comments = db.Column(db.String(500))
    is_new = db.Column(db.Boolean)
    taken_by = db.Column(db.Integer, db.ForeignKey('users.id'))

whooshalchemy.whoosh_index(app, Rates)