"""Data Trust Logger Application."""
from flask import Flask
from flask_cors import CORS

from data_trust_logger.api import (data_resources_health_bp, log_bp,
                                   mci_health_bp)


def create_app(environment: str = None):
    """Create the Flask application.

    Returns:
        obj: The configured Flask application context

    """

    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(mci_health_bp)
    app.register_blueprint(data_resources_health_bp)
    app.register_blueprint(log_bp)

    return app
