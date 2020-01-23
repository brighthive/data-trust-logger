"""Data Resources Health Check API.

A simple API for returning health statistics from Data Resources.

"""

from flask import Blueprint, request
from flask_restful import Api, Resource
from sqlalchemy import MetaData, Table, create_engine

import data_trust_logger.utilities.fake_results as fake
from data_trust_logger.config import ConfigurationFactory
import data_trust_logger.utilities.responses as resp
from data_trust_logger.utilities.health_helper import (
    get_endpoint_record_count, get_endpoint_status)

config = ConfigurationFactory.from_env()


class DataResourcesHealthCheckResource(Resource):
    """Health Check API."""

    def __init__(self):
        self.response = resp.ResponseBody()
        self.endpoints = ['/programs', '/providers', '/credentials', '/referrals']

    def get(self):
        engine = create_engine(config.DR_DATABASE_URI)
        table_names = engine.table_names()
        tables = ['alembic_version', 'checksums', 'logs']
        endpoints = [endpoint for endpoint in table_names if endpoint not in tables and "\\" not in endpoint]

        endpoints_msg = {'endpoints': []}
        for endpoint in endpoints:
            status = get_endpoint_status(f"{config.MCI_URL}/{endpoint}")
            count = get_endpoint_record_count(engine, endpoint)
            
            endpoints_msg['endpoints'].append({
                'endpoint': endpoint,
                'record_count': count,
                'endpoint_health': status
            })

        return self.response.get_one_response(endpoints_msg)


data_resources_health_bp = Blueprint('data_resources_health_ep', __name__)
data_resources_health_api = Api(data_resources_health_bp)
data_resources_health_api.add_resource(DataResourcesHealthCheckResource, '/health/data_resources')
