"""Data Trust Logger Application."""
import brighthive_authlib
from brighthive_authlib import OAuth2ProviderError
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api

from flask import Blueprint

from data_trust_logger.api import health_bp, log_bp


def handle_errors(e):
    print("Incoming error:", e)
    if isinstance(e, OAuth2ProviderError):
        response = jsonify({'message': 'Access Denied'})
        response.status_code = 401
        return response
    else:
        response = jsonify({'error': 'An unknown error occured'})
        response.status_code = 400
        return response

def create_app(environment: str = None):
    """Create the Flask application.

    Returns:
        obj: The configured Flask application context

    """

    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(log_bp)

    app.register_error_handler(Exception, handle_errors)

    return app
