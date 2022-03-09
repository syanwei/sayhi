# -*- coding: utf-8 -*-
"""
    :author: Mamba Song
    :copyright: © 2022 Mamba Song <songyw.py@gmail.com>
    :software: PyCharm
"""
from marshmallow import fields, validate, Schema

_password_rule = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$'


class SignupSchema(Schema):
    """signup"""
    username = fields.String(required=True, validate=validate.Length(min=5, max=20))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Regexp(_password_rule))


class LoginSchema(Schema):
    """username login """
    username = fields.String(required=False, validate=validate.Length(min=5, max=20))
    email = fields.Email(required=False)
    password = fields.String(required=True, validate=validate.Regexp(_password_rule))
    remember = fields.Boolean(required=True)
    login_type = fields.Int(required=True, validate=validate.Range(1, 2), doc='1:login by username; 2:login by email')


class CommentSchema(Schema):
    """comment"""
    comment = fields.String(required=True, validate=validate.Length(min=3, max=200))
    parent_id = fields.Int(required=True, validate=validate.Range(min=0))
