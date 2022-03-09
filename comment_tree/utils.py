# -*- coding: utf-8 -*-
"""
    :author: Mamba Song
    :copyright: © 2022 Mamba Song <songyw.py@gmail.com>
    :software: PyCharm
"""
import uuid

from flask import jsonify


def json_resp(code=0, msg='', data=None, request_id=None):
    if data is None:
        data = {}
    if request_id is None:
        request_id = uuid.uuid4().hex[:10]

    return_dict = {
        'code': code,
        'msg': msg,
        'data': data,
        'request_id': request_id
    }

    return jsonify(**return_dict)


def success_resp(data=None):
    return json_resp(code=0, msg="success", data=data)


def fail_resp(code, msg):
    return json_resp(code=code, msg=msg)
