import os
from flask import Flask
from . import views
from flask_marshmallow import Marshmallow


def create_app():
    app = Flask(__name__)

    app.register_blueprint(views.main_bp)

    env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
    app.config.from_object(env_config)
    # ma = Marshmallow(app)

    return app