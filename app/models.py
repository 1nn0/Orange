from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100), unique = True)
    role = db.Column(db.Integer, default = ROLE_USER)
    operations = db.relationship('Operation', backref = 'user_id', lazy = 'dynamic')

    def __repr__(self):
        return '<User %r>' % (self.login)
