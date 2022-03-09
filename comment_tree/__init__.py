# -*- coding: utf-8 -*-
"""
    :author: Mamba Song
    :copyright: © 2022 Mamba Song <songyw.py@gmail.com>
    :software: PyCharm
"""
import json
import logging
import os
import time
import traceback
import uuid
from logging.handlers import RotatingFileHandler
from functools import wraps

import click
from flask import Flask, request, g, session
from flask_sqlalchemy import get_debug_queries
from werkzeug.exceptions import HTTPException

from comment_tree.extensions import db, moment, toolbar, migrate, RequestMethodError, SchemaError, ParameterError, \
    NotLoginError, bootstrap
from comment_tree.fakes import fake_user
from comment_tree.models import User, Comment
from comment_tree.settings import config
from comment_tree.utils import json_resp

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('comment_tree')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_request_handlers(app)
    return app


def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    formatter = logging.Formatter('%(time)s - %(name)s - %(level_name)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/comment_tree.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    from comment_tree.blueprints.auth import auth_bp
    from comment_tree.blueprints.comment import comment_bp
    from comment_tree.blueprints.static import static_bp
    app.register_blueprint(static_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(comment_bp, url_prefix='/tree')


def register_errors(app):
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response

    @app.errorhandler(ParameterError)
    def parameter_error(error):
        return json_resp(40001, error.args[0])

    @app.errorhandler(SchemaError)
    def parameter_error(error):
        return json_resp(40002, error.args[0])

    @app.errorhandler(RequestMethodError)
    def request_method_error(error):
        return json_resp(40003, error.args[0])

    @app.errorhandler(NotLoginError)
    def not_login_error(error):
        return json_resp(40004, error.args[0])

    @app.errorhandler(Exception)
    def error_500(error):
        traceback_error = traceback.format_exc()
        request_id = uuid.uuid4().hex[:10]
        parameter = g.request_data
        app.logger.error(
            f"service 500 error\n"
            f"request_id: {request_id}\n"
            f"uri: {request.url_rule}\n"
            f"parameter: {parameter}\n"
            f"error: {error.args}\n\n"
            f"{traceback_error}\n"
        )
        return json_resp(50000, "this error has been recorded, we will get it fixed", request_id=request_id)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """Building user, just for you."""

        click.echo('Initializing the database...')
        db.create_all()

        user = User.query.filter_by(username=username).first()
        if user is not None:
            click.echo('The user already exists, updating...')
            user.username = username
            user.set_password(password)
            db.session.commit()
        else:
            click.echo('Creating the temporary user account...')
            fake_user(username, password)
        click.echo('Done.')

    @app.cli.command()
    @click.option('--comment', default=50, help='Quantity of comments, default is 50.')
    def forge(comment):
        """Generate fake data."""
        from comment_tree.fakes import fake_users, fake_comments

        db.drop_all()
        db.create_all()

        fake_users(comment)
        click.echo('Generating %d user...' % comment)

        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)

        click.echo('Done.')


def register_request_handlers(app):
    @app.after_request
    def _after_request(response):
        for q in get_debug_queries():
            if q.duration >= app.config['SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
                    % (q.duration, q.context, q.statement)
                )
        return response

    @app.before_request
    def _before_request():
        if request.path == f"/health":
            return
        data = {}
        if request.method in ['POST', 'PUT', 'DELETE']:
            data = request.get_json(silent=True) or request.data
        elif request.method == 'GET':
            data = request.args
        elif request.method not in ['OPTIONS']:
            raise RequestMethodError("Unsupported request method")
        g.force_master = False
        g.key = request.headers.get('Authorization', '')
        g.start = int(time.time() * 1000)
        g.user_id = ''
        if "user_id" in session:
            g.user_id = session["user_id"]

        g.request_data = data


def expects_receive(json_schema=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            form = g.request_data
            if json_schema is not None:
                errors = json_schema().validate(form)
                if errors:
                    raise SchemaError(str(errors))
            return f(*args, **kwargs)

        return wrapper

    return decorator


def user_required(f):
    @wraps(f)
    def func(*args, **kwargs):
        if not g.user_id:
            raise NotLoginError("login required")
        _user = User.query.first()
        if not _user:
            raise NotLoginError("login required")
        g.user = _user
        return f(*args, **kwargs)

    return func
