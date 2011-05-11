# coding:utf-8
# Copyright 2011 Litl, LLC. All Rights Reserved.

import logging
import unittest

from flask import url_for
import portal.app
from portal.models import PortalUser
from portal.models import db
from bson import ObjectId

class PortalTestCase(unittest.TestCase):

    def setUp(self):
        db.users.drop()
        self.app = portal.app.create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def test_list_users(self):
        response = self.client.get('/bootstrap/')
        response = self.client.get("/user/all/")
        assert response.status_code == 200

    def test_user_model(self):
        user = PortalUser(email="test@test.com", first_name="Test", last_name="User")
        user.put()
        assert PortalUser.find_by_email("test@test.com")

        assert PortalUser.find_by_key(ObjectId()) == None

    def test_create_user(self):
        response = self.client.get('/bootstrap/')
        response = self.client.get('/user/create/')
        assert response.status_code == 200
        test_data = { "email": 'create_test@test.com',
                      "first_name": "create",
                      "last_name": "test",
                      "password": "password",
                      "confirm": "password",
                      "needs_password": True,
                    }
        response = self.client.post('/user/save/', data=test_data, follow_redirects=True)
        assert response.status_code == 200
        user = PortalUser.find_by_email(test_data['email'])
        assert user
        assert user.first_name == test_data['first_name']
        assert user.last_name == test_data['last_name']

        # save with a new name, test false "needs_password" path
        test_data = { "email": 'create_test@test.com',
                      "first_name": "changed",
                      "last_name": "test",
                    }
        response = self.client.post('/user/save/', data=test_data, follow_redirects=True)
        assert response.status_code == 200
        user = PortalUser.find_by_email("create_test@test.com")
        assert user.first_name == "changed"

        # test error case -- first_name can't be blank
        test_data = { "email": 'create_test@test.com',
                      "first_name": "",
                      "last_name": "test",
                    }
        response = self.client.post('/user/save/', data=test_data, follow_redirects=True)
        assert response.status_code == 200
        user = PortalUser.find_by_email("create_test@test.com")
        assert user.first_name is not ""

    def test_require_login(self):
        # not logged in so get a redirect
        response = self.client.get('/user/create/')
        assert response.status_code == 302

        # same for saving a user
        test_data = { "email": 'create_test@test.com',
                      "first_name": "create",
                      "last_name": "test",
                    }
        response = self.client.post('/user/save/', data=test_data, follow_redirects=False)
        assert response.status_code == 302

        # same for listing
        response = self.client.get('/user/all/')
        assert response.status_code == 302

    def test_passwords(self):
        user = PortalUser(email="test@test.com", first_name="Test", last_name="User")
        user.set_password("password")
        user.put()
        assert PortalUser.check_login("test@test.com", "password")
        assert not PortalUser.check_login("wrong@test.com", "password")
        assert not PortalUser.check_login("test@test.com", "wrong")

    def test_login(self):
        user = PortalUser(email="test@test.com", first_name="Test", last_name="User")
        user.set_password("password")
        user.put()
        response = self.client.get('/login')
        assert response.status_code == 200

        # bogus logins cause errors
        # TODO -- test that session is not set
        login_data = { "email": "bogus@wrong.com", "password": "password"}
        response = self.client.post('/login', data=login_data)
        assert "Invalid" in response.data
        login_data = { "email": "test@test.com", "password": "wrong"}
        response = self.client.post('/login', data=login_data)
        assert "Invalid" in response.data

        login_data = { "email": "test@test.com", "password": "password"}
        response = self.client.post('/login', data=login_data, follow_redirects=True)
        assert "Invalid" not in response.data
        assert "You were logged in" in response.data

        # now we can get
        response = self.client.get('/user/all/')
        assert response.status_code == 200

    def test_bootstrap_error(self):
        user = PortalUser(email="test@test.com", first_name="Test", last_name="User")
        user.put()
        response = self.client.get('/bootstrap/')
        # since we have a user now, bootstrap should fail
        response = self.client.get('/user/create/')
        logging.info("response status: %s" % response.status_code)
        assert response.status_code == 302

    def test_change_password(self):
        user = PortalUser(email="test@test.com", first_name="Test", last_name="User")
        user.set_password("password")
        user.put()
        login_data = { "email": "test@test.com", "password": "password"}
        response = self.client.post('/login', data=login_data, follow_redirects=True)

        response = self.client.get('/user/test@test.com/change_password/')
        assert response.status_code == 200

        pw_data = {"password": "newpassword", "confirm": "newpassword"}
        response = self.client.post('/user/test@test.com/change_password/', data=pw_data, follow_redirects=True)
        assert response.status_code == 200
        assert PortalUser.check_login("test@test.com", "newpassword")
        assert not PortalUser.check_login("test@test.com", "password")
        self.client.get("/logout")
        login_data = { "email": "test@test.com", "password": "newpassword"}
        response = self.client.post('/login', data=login_data, follow_redirects=True)
        assert "Invalid" not in response.data
        assert "You were logged in" in response.data

    def test_change_email(self):
        user = PortalUser(email="test@test.com", first_name="Test", last_name="User")
        user.set_password("password")
        id = user.put()
        login_data = { "email": "test@test.com", "password": "password"}
        response = self.client.post('/login', data=login_data, follow_redirects=True)
        test_data = { "email": 'newemail@test.com',
                      "first_name": "Test",
                      "last_name": "User",
                      "id": str(id),
                    }
        response = self.client.post('/user/save/', data=test_data, follow_redirects=False)
        assert PortalUser.find_by_email("newemail@test.com")
        assert PortalUser.check_login("newemail@test.com", "password")

