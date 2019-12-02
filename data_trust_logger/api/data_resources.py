"""Data Resources Health Check API.

A simple API for returning health statistics from Data Resources.

"""

from flask import Blueprint, request
from flask_restful import Resource, Api

import data_trust_logger.utilities.responses as resp
import data_trust_logger.utilities.fake_results as fake


class DataResourcesHealthCheckResource(Resource):
    """Health Check API."""

    def __init__(self):
        self.response = resp.ResponseBody()
        self.endpoints = ['/programs', '/providers', '/credentials', '/referrals']

    def get(self):
        # TODO: This method should retrieve values from the various data resource APIs in the future
        return self.response.get_one_response(fake.generate_fake_results(self.endpoints))


data_resources_health_bp = Blueprint('data_resources_health_ep', __name__)
data_resources_health_api = Api(data_resources_health_bp)
data_resources_health_api.add_resource(DataResourcesHealthCheckResource, '/health/data_resources')
