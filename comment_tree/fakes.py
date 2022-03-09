# -*- coding: utf-8 -*-
"""
    :author: Mamba Song
    :copyright: © 2022 Mamba Song <songyw.py@gmail.com>
    :software: PyCharm
"""
from faker import Faker

from comment_tree.extensions import db
from comment_tree.models import User, Comment

fake = Faker()


def fake_users(count=50):
    for i in range(count):
        admin = User(
            username='mamba%d' % i,
            email="song%d.py@gmail.com" % i
        )
        admin.set_password('12341aA&')
        db.session.add(admin)
    db.session.commit()


def fake_user(username, password):
    admin = User(
        username=username,
        email="songyw.py@gmail.com"
    )
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()


def fake_comments(count=50):
    for i in range(count):
        comment = Comment(
            user_id=i,
            username='mamba%d' % i,
            comment=fake.sentence(),
            parent_id=i,
            created_at=fake.date_time_this_year(),
        )
        db.session.add(comment)
    db.session.commit()
