
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence, desc, func, distinct
from werkzeug.exceptions import NotFound
from flask import url_for, current_app
from sqlalchemy.orm import relationship, backref
from elasticsearch import Elasticsearch, RequestsHttpConnection

from werkzeug.security import gen_salt, generate_password_hash, check_password_hash
from datetime import datetime, timedelta, date
from flask_security import UserMixin, RoleMixin
import os
import importlib

import sys

# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

TYPE_BANK_SLIP_PAYMENT = 2
TYPE_CREDIT_CARD_PAYMENT = 1
mname = os.environ['APP_SETTINGS'].split('.')[0]
cname = os.environ['APP_SETTINGS'].split('.')[1]
module = importlib.import_module(mname)
curr_config = getattr(module, cname)


es = Elasticsearch()
db = SQLAlchemy()

def result2dict(result, attrs):
    d = []
    for row in result:
        di = {}
        for attr in attrs:
            value = getattr(row, attr)
            if isinstance(value, basestring):
                value = value.encode('utf-8')
            di[attr] = value
        d.append(di)

    return d


def result2list(result, attr):
    d = []
    for row in result:
        attrvalue = getattr(row, attr)
        d.append(attrvalue.encode('utf-8'))

    return d


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(20), index=True)
    hashpw = db.Column('password', db.String(250))
    email = db.Column('email', db.String(80), unique=True, index=True)
    social_id = db.Column(db.String(64), unique=True)
    nickname = db.Column(db.String(64))
    roles = relationship("Role", secondary="roleuser", viewonly=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password=None, name=None, social_id=None, nickname=None, admin=False):
        self.name = name
        if password:
            self.set_password(password)
        self.email = email
        self.social_id = social_id
        self.nickname = nickname
        self.admin = admin

    def set_password(self, password):
        self.hashpw = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashpw, password)

    def get_id(self):
        return unicode(self.id)

    def to_json(self):
        json = {
            'url': self.get_url(),
            'user_id': self.id,
            'name': self.name,
            'email': self.email
        }
        return json

    def get_url(self):
        return url_for('api.get_user', email=self.email, _external=True)

    def __repr__(self):
        return '<User %r>' % (self.name)
