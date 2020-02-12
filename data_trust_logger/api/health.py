"""Health Audit API.

A simple API for returning health metrics about the MCI and DR APIs.

"""
import json

from brighthive_authlib import token_required
from flask import Blueprint, request
from flask_restful import Api, Resource
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

import data_trust_logger.utilities.responses as resp
from data_trust_logger.config import ConfigurationFactory

config = ConfigurationFactory.from_env()


class HealthAuditResource(Resource):
    """Health Audit API."""

    def __init__(self):
        self.response = resp.ResponseBody()

    @token_required(config.oauth2_provider)
    def get(self):
        metrics_data = {}

        with open('/tmp/metrics_blob.json') as json_data:
            metrics_data = json.load(json_data)

        return self.response.get_one_response(metrics_data)


health_bp = Blueprint('health_ep', __name__)
health_api = Api(health_bp)
health_api.add_resource(HealthAuditResource, '/health')
