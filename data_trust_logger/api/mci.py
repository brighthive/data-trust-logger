"""MCI Health Check API.

A simple API for returning health statistics from MCI.

"""

from flask import Blueprint, request
from flask_restful import Api, Resource
from sqlalchemy import create_engine

import data_trust_logger.utilities.responses as resp
from data_trust_logger.config import ConfigurationFactory
# from data_trust_logger.utilities.health_helper import generate_endpoints_blob

config = ConfigurationFactory.from_env()


class MCIHealthCheckResource(Resource):
    """Health Check API."""

    def __init__(self):
        self.response = resp.ResponseBody()
        self.endpoints = ['users', 'source', 'gender', 'address', 'disposition', 'ethnicity',
                          'employment_status', 'education_level']
        self.table_to_ep_mappings = {
            'users': 'individual',
            'ethnicity': 'ethnicity_race',
        }

    def get(self):
        engine = create_engine(config.mci_psql_uri)

        # Rather than calling this function, we can retrieve the data from a database.
        # endpoints_blob = generate_endpoints_blob(engine, config.mci_url, self.endpoints, self.table_to_ep_mappings)
        endpoints_blob = {}

        return self.response.get_one_response(endpoints_blob)


mci_health_bp = Blueprint('mci_health_ep', __name__)
mci_health_api = Api(mci_health_bp)
mci_health_api.add_resource(MCIHealthCheckResource, '/health/mci')
