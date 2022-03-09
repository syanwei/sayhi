# -*- coding: utf-8 -*-
"""
    :author: Mamba Song
    :copyright: © 2022 Mamba Song <songyw.py@gmail.com>
    :software: PyCharm
"""
import os

from flask import Blueprint, send_from_directory

static_bp = Blueprint('static', __name__)


@static_bp.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.getcwd(), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
