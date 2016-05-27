import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'fuckmybrain'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://techgrp_flask:gfhjkmgfhjkm@clarus.timeweb.ru/techgrp_flask'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_POOL_RECYCLE = 20
SQLALCHEMY_TRACK_MODIFICATIONS = True

WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 500

ITEMS_PER_PAGE = 50

