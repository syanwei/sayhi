# -*- coding: utf-8 -*-
"""
    :author: Mamba Song
    :copyright: © 2022 Mamba Song <songyw.py@gmail.com>
    :software: PyCharm
"""
from flask import Blueprint, g

from comment_tree import expects_receive, db, user_required
from comment_tree.schema import CommentSchema
from comment_tree.models import Comment
from comment_tree.utils import success_resp

comment_bp = Blueprint('tree', __name__)


@comment_bp.route('/comment', methods=['POST'])
@expects_receive(json_schema=CommentSchema)
@user_required
def add_comment():
    form = g.request_data
    comment = form['comment']
    parent_id = form['parent_id']
    comm = Comment(username=g.user.username, user_id=g.user_id, comment=comment, parent_id=parent_id)
    db.session.add(comm)
    db.session.commit()
    # TODO cache comment_tree after new comment
    return success_resp()


@comment_bp.route('/comments', methods=['GET'])
def get_comments():
    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    dict_comments = [
        {'id': c.id, 'parent_id': c.parent_id, 'username': c.username, 'created_at': c.created_at, 'comment': c.comment}
        for c in comments
    ]

    def dept_trees(parent_id=0):
        data_list = [i for i in dict_comments if i['parent_id'] == parent_id]
        if len(data_list) > 0:
            data = []
            for dept in data_list:
                children_list = dept_trees(dept['id'])
                if children_list:
                    dept['children'] = children_list
                data.append(dept)
            return data
        return []

    comment_data = dept_trees(0)
    return success_resp(comment_data)
