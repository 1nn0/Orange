import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'fuckmybrain'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://techgrp_flaskdev:l6MUcdMt@clarus.timeweb.ru/techgrp_flaskdev'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_POOL_RECYCLE = 20
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = 'change_me'
SECURITY_TRACKABLE = True
SECURITY_REMEMBER_SALT = 'remember_salt_change_me'


WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 500

ITEMS_PER_PAGE = 50

