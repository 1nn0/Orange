import flask.ext.whooshalchemy as whooshalchemy

from app import app, db

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True,)
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), unique=True)
    role = db.Column(db.Integer, default=ROLE_USER)
    last_login = db.Column(db.DATETIME)

    def __repr__(self):
        return '<User %r>' % (self.login)


class Operations(db.Model):
    __tablename__ = 'operations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    operation = db.Column(db.String(200))
    timestamp = db.Column(db.TIMESTAMP)


class Sprav(db.Model):
    __tablename__ = 'tb1'
    __searchable__ = ['dolzh', 'name', 'fname', 'tel_loc', 'kab']
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dolzh = db.Column(db.String(100))
    org = db.Column(db.String(100))
    name = db.Column(db.String(100))
    fname = db.Column(db.String(100))
    sname = db.Column(db.String(100))
    str = db.Column(db.String(100))
    kor = db.Column(db.String(100))
    kab = db.Column(db.String(100))
    tel = db.Column(db.String(100))
    tel_loc = db.Column(db.String(100))
    tel_mob = db.Column(db.String(100))
    email = db.Column(db.String(120))

whooshalchemy.whoosh_index(app, Sprav)