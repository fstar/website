# -*- coding:utf-8 -*-
import re
import sys
import time

from flask import Flask, request, render_template
from flask_wtf.csrf import CsrfProtect
from flask_cors import CORS
from flask_pymongo import PyMongo

from app.common.log import create_logger_handler
from app.models import db


mongo_client = PyMongo()

def create_app(database, config="app.config.ConfigObject"):
    app = Flask(__name__)
    CORS(app)
    initialize_app(application=app, config=config)
    database.init_app(app)
    database.create_all(app=app)
    mongo_client.init_app(app=app)

    app.logger_name = "spider_api"
    app.logger.handlers = create_logger_handler("spider_api", is_stream_handler=True)

    add_request_handler(application=app, database=database)


    return app



def initialize_app(application, config, profile=False):
    # 读取配置
    application.config.from_object(config)


    # 注册蓝图
    from app.views.login.login_view import login_view
    from app.views.index.index_view import index_view
    from app.views.admin.admin_view import admin_view
    # from app.views.input_data.input_api import input_data_api_view
    # from app.views.data.data_view import data_view
    # from app.views.input_mongodb.input_api import input_mongodb_api_view

    application.register_blueprint(login_view)
    application.register_blueprint(index_view)
    application.register_blueprint(admin_view)
    # application.register_blueprint(input_data_api_view)
    # application.register_blueprint(data_view)
    # application.register_blueprint(input_mongodb_api_view)


    # restful api 不跨域保护
    csrf = CsrfProtect()
    csrf.init_app(application)

    # csrf.exempt(input_data_api_view)
    csrf.exempt(login_view)
    csrf.exempt(admin_view)
    # csrf.exempt(data_view)
    # csrf.exempt(input_mongodb_api_view)


def add_request_handler(application, database):
    @application.before_request
    def before_request():
        request.start_time = time.time()

    @application.after_request
    def after_request(response):
        start_time = getattr(request, "start_time", 0)
        use_time = 0
        if start_time:
            use_time = round((time.time() - start_time) * 1000, 3)
        method = request.method
        status_code = response.status_code
        url = re.sub("http://.*?/", "/", request.url)
        application.logger.info("%s %s %s-->cost:%s ms" % (method, status_code, url, use_time))
        return response

    @application.teardown_request
    def teardown_request(exception):
        database.session.close() # make sure that db session is closed successfully
        if exception:
            start_time = getattr(request, "start_time", 0)
            use_time = 0
            if start_time:
                use_time = round((time.time() - start_time) * 1000, 3)
            method = request.method
            url = re.sub("http://.*?/", "/", request.url)
            form_data = {}
            form_data.update(request.form)
            form_data.update(request.args)
            application.logger.error("%s %s -->cost:%s ms, form_data: %s" % (url, method, use_time, str(form_data)))
            application.logger.error(exception, exc_info=1)

    @application.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404
app = create_app(db)
app.jinja_env = app.jinja_env.overlay(cache_size=0)
