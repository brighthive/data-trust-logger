"""Data Trust Logger Application."""
from flask import Flask
from flask_cors import CORS

from data_trust_logger.api import health_bp, log_bp


def create_app(environment: str = None):
    """Create the Flask application.

    Returns:
        obj: The configured Flask application context

    """

    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(log_bp)

    return app
