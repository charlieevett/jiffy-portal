# coding:utf-8
# Copyright 2011 Litl, LLC. All Rights Reserved.

from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy

def create_app():
    app = Flask(__name__)
    app.config.from_object('portal.settings')
    app.config['MONGOALCHEMY_DATABASE'] = 'portal'

    from portal.models import db
    db.init_app(app)

    from portal.login import door
    app.register_module(door)

    from portal.users import portal
    app.register_module(portal)

    return app
