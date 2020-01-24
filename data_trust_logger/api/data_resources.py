"""Data Resources Health Check API.

A simple API for returning health statistics from Data Resources.

"""

from flask import Blueprint, request
from flask_restful import Api, Resource
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

import data_trust_logger.utilities.responses as resp
from data_trust_logger.config import ConfigurationFactory
from data_trust_logger.utilities.health_helper import generate_endpoints_blob

config = ConfigurationFactory.from_env()


class DataResourcesHealthCheckResource(Resource):
    """Health Check API."""

    def __init__(self):
        self.response = resp.ResponseBody()

    def get(self):
        engine = create_engine(config.dr_psql_uri)

        try:
            table_names = engine.table_names()
        except OperationalError:
            table_names = []

        metatables = ['alembic_version', 'checksums', 'logs']
        endpoints = [endpoint for endpoint in table_names if endpoint not in metatables and "\\" not in endpoint]
        
        endpoints_blob = generate_endpoints_blob(engine, config.dr_url, endpoints)

        return self.response.get_one_response(endpoints_blob)


data_resources_health_bp = Blueprint('data_resources_health_ep', __name__)
data_resources_health_api = Api(data_resources_health_bp)
data_resources_health_api.add_resource(DataResourcesHealthCheckResource, '/health/data_resources')
