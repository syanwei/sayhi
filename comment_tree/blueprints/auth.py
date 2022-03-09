# -*- coding: utf-8 -*-
"""
    :author: Mamba Song
    :copyright: © 2022 Mamba Song <songyw.py@gmail.com>
    :software: PyCharm
"""
from flask import Blueprint, session, g
from sqlalchemy import or_

from comment_tree import db, expects_receive, user_required
from comment_tree.schema import LoginSchema, SignupSchema
from comment_tree.models import User
from comment_tree.utils import json_resp, fail_resp, success_resp

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
@expects_receive(json_schema=LoginSchema)
def login():
    form = g.request_data
    username = form.get('username')
    email = form.get('email')
    password = form['password']
    remember = form['remember']
    login_type = form['login_type']

    # 1:login by username; 2:login by email
    if login_type == 1:
        user = User.query.filter_by(username=username).first()
    else:
        user = User.query.filter_by(email=email).first()
    if user and user.validate_password(password):
        session["user_id"] = user.id
        if remember:
            session.permanent = True
        resp_data = {
            "username": user.username,
            "email": user.email,
        }
        return success_resp(resp_data)
    return fail_resp(40001, 'Invalid username or password')


@auth_bp.route('/signup', methods=['POST'])
@expects_receive(json_schema=SignupSchema)
def signup():
    form = g.request_data
    username = form['username']
    password = form['password']
    email = form['email']
    # check if username or email exists
    _user = User.query.filter(or_(User.username == username, User.email == email)).first()
    if _user is not None:
        return json_resp(40001, 'username or email is already signup')
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return success_resp()


@auth_bp.route('/logout', methods=['GET'])
@user_required
def logout():
    session.clear()
    return success_resp()
