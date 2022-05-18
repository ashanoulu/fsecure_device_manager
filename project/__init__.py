"""
Init file
"""
from flask import Flask
from flasgger import Swagger
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
cache = Cache()


def create_app(test_config=None):
    """
    method to create application
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config["SWAGGER"] = {
        "title": "Device Manager API",
        "openapi": "3.0.3",
        "uiversion": 3,
    }
    swagger = Swagger(app, template_file="doc/devicemanager.yml")

    app.config["CACHE_TYPE"] = "simple"
    # app.config["CACHE_DIR"] = "cache"

    db.init_app(app)
    cache.init_app(app)

    from . import api

    app.register_blueprint(api.api_bp)

    return app
