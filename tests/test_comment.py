# -*- coding: utf-8 -*-
"""
    :author: Mamba Song
    :copyright: © 2022 Mamba Song <songyw.py@gmail.com>
    :software: PyCharm
"""
import json

from flask import url_for

from comment_tree.models import Comment
from comment_tree.extensions import db

from tests.base import BaseTestCase


class CommentTestCase(BaseTestCase):

    def setUp(self):
        super(CommentTestCase, self).setUp()
        self.login()

        comment = Comment(comment='A comment', parent_id=0)

        db.session.add(comment)
        db.session.commit()

    def test_new_comment(self):
        response = self.client.post(url_for('tree.add_comment'), headers={'Content-Type': 'application/json'},
                                    data=json.dumps({
                                        "comment": 'I am an new comment.',
                                        "parent_id": 1
                                    }))
        data = response.get_data(as_text=True)
        self.assertIn('code":0,"data":{},"msg":"success', data)

    def test_get_comments(self):
        response = self.client.get(url_for('tree.get_comments'))
        data = response.get_data(as_text=True)
        self.assertIn('comment":"A comment"', data)
