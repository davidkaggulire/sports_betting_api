import os
from flask import Flask
from flask_cors import CORS
from . import views


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(views.main_bp)

    env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
    app.config.from_object(env_config)
    return app
