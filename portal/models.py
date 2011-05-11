# coding:utf-8
# Copyright 2011 Litl, LLC. All Rights Reserved.
import calendar
from datetime import datetime
from simplejson import dumps
import logging
from werkzeug import generate_password_hash, check_password_hash

from pymongo import Connection
from pymongo.objectid import ObjectId

connection = Connection()
db = connection.test_database

class PortalUser(object):

    def __init__(self, first_name="", last_name="", email="", password_hash="", dict=None):
        if dict:
            self.__dict__.update(dict)
            return

        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = password_hash

    def get_id(self):
        return self._id

    def set_id(self, value):
        # can't change the id
        pass

    id = property(get_id, set_id)

    @classmethod
    def find_by_email(cls, email):
        raw_user = db.users.find_one({"email": email})
        if raw_user:
            user = PortalUser(dict=raw_user)
            return user
        else:
            return None

    @classmethod
    def find_by_key(cls, key):
        raw_user = db.users.find_one({"_id": ObjectId(key)})
        if raw_user:
            return PortalUser(dict=raw_user)
        else:
            return None

    @classmethod
    def all(cls):
        return db.users.find()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return self.password_hash and check_password_hash(self.password_hash, password)

    @classmethod
    def check_login(cls, email, password):
        user = cls.find_by_email(email)
        return user and user.check_password(password)

    @classmethod
    def no_users(cls):
        return db.users.count() == 0

    def put(self):
        json = dict(self.__dict__)
        users = db.users
        return users.save(json)

