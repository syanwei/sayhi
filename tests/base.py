# -*- coding: utf-8 -*-
"""
    :author: Mamba Song
    :copyright: © 2022 Mamba Song <songyw.py@gmail.com>
    :software: PyCharm
"""
import json
import unittest

from flask import url_for

from comment_tree import create_app
from comment_tree.extensions import db
from comment_tree.models import User


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

        db.create_all()
        user = User(username='mambaSong', email="songyw.py@gmail.com")
        user.set_password('123456aA!')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def login(self, username='mambaSong', password='123456aA!', email='songyw.py@gmail.com', login_type=1):
        return self.client.post(url_for('auth.login'), headers={'Content-Type': 'application/json'},
                                data=json.dumps({
                                    "username": username,
                                    "password": password,
                                    "email": email,
                                    "login_type": login_type,
                                    "remember": True
                                }))

    def logout(self):
        return self.client.get(url_for('auth.logout'))
