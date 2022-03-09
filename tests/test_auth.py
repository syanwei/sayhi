# -*- coding: utf-8 -*-
"""
    :author: Mamba Song
    :copyright: © 2022 Mamba Song <songyw.py@gmail.com>
    :software: PyCharm
"""
from tests.base import BaseTestCase


class AuthTestCase(BaseTestCase):

    def test_login_user(self):
        response = self.login()
        data = response.get_data(as_text=True)
        self.assertIn('"code":0,"data":{"email":"songyw.py@gmail.com","username":"mambaSong"},"msg":"success"', data)

    def test_fail_login_username(self):
        response = self.login(username='wrongUsername', password='123456aA!', login_type=1)
        data = response.get_data(as_text=True)
        self.assertIn('code":40001,"data":{},"msg":"Invalid username or password', data)

    def test_fail_login_email(self):
        response = self.login(password='123456aA@', email="songyw.py@gmail.com", login_type=2)
        data = response.get_data(as_text=True)
        self.assertIn('code":40001,"data":{},"msg":"Invalid username or password', data)

    def test_fail_login_password(self):
        response = self.login(password='12345678', email="songyw.py@gmail.com", login_type=2)
        data = response.get_data(as_text=True)
        self.assertIn('password\': [\'String does not match expected pattern.', data)

    def test_logout_user(self):
        self.login()
        response = self.logout()
        data = response.get_data(as_text=True)
        self.assertIn('{"code":0,"data":{},"msg":"success"', data)

