from flask import Flask

from src.presentation.flask import user


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    config_module = f"src.application.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)
    app.register_blueprint(user.blueprint)

    return app
