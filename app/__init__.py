# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config


login_manage = LoginManager()
login_manage.session_protection = "strong"
login_manage.login_view = "auth.login"

db = SQLAlchemy()


def create_app(config_name):
    from app.dataset.views import dataset
    from app.docker.views import docker_control
    from app import models

    app = Flask(__name__)
    app.register_blueprint(dataset, url_prefix="/dataset")
    app.register_blueprint(docker_control, url_prefix="/docker")
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manage.init_app(app)
    return app
