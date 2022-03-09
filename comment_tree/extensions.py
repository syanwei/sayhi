# -*- coding: utf-8 -*-
"""
    :author: Mamba Song
    :copyright: © 2022 Mamba Song <songyw.py@gmail.com>
    :software: PyCharm
"""
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
toolbar = DebugToolbarExtension()
migrate = Migrate()


class ParameterError(Exception):
    pass


class NotLoginError(Exception):
    pass


class RequestMethodError(Exception):
    pass


# Parameter format check error
class SchemaError(Exception):
    pass
