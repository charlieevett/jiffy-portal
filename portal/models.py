# coding:utf-8
# Copyright 2011 Litl, LLC. All Rights Reserved.
import logging
from werkzeug import generate_password_hash, check_password_hash

from flaskext.mongoalchemy import MongoAlchemy
from pymongo.objectid import ObjectId

db = MongoAlchemy()

class PortalUser(db.Document):

    email = db.StringField()
    first_name = db.StringField(required=False)
    last_name = db.StringField(required=False)
    password_hash = db.StringField(required=False, default="")

    def get_id(self):
        return self.mongo_id

    def set_id(self, value):
        # can't change the id
        pass

    id = property(get_id, set_id)

    @classmethod
    def find_by_email(cls, email):
        return PortalUser.query.filter({"email": email}).first()

    @classmethod
    def find_by_key(cls, key):
        return PortalUser.query.filter({"mongo_id": ObjectId(key)}).first()

    @classmethod
    def all(cls):
        return PortalUser.query.all()

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
        return PortalUser.query.count() == 0

