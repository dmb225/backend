import os

from flask import Flask

from src.presentation.flask import root, user


def create_app(config_name: str) -> Flask:
    #setup_logging()

    #logger = logging.getLogger(__name__)
    #logger.info("Creating Flask app...")
    #logger.info(f"FLASK_CONFIG: {config_name}")

    config_module = f"src.application.config.{config_name.capitalize()}Config"

    app = Flask(__name__)
    app.config.from_object(config_module)
    app.register_blueprint(root.blueprint)
    app.register_blueprint(user.blueprint)

    return app


app = create_app(os.environ["FLASK_CONFIG"])
