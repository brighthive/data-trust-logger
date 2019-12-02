"""MCI Health Check API.

A simple API for returning health statistics from MCI.

"""

from flask import Blueprint, request
from flask_restful import Resource, Api

import data_trust_logger.utilities.responses as resp
import data_trust_logger.utilities.fake_results as fake


class MCIHealthCheckResource(Resource):
    """Health Check API."""

    def __init__(self):
        self.response = resp.ResponseBody()
        self.endpoints = ['/mci/users', '/mci/source', '/mci/gender', '/mci/address', '/mci/disposition', '/mci/ethnicity',
                          '/mci/employment_status', '/mci/education_level']

    def get(self):
        # TODO: This method should retrieve values from the MCI in the future
        return self.response.get_one_response(fake.generate_fake_results(self.endpoints))


mci_health_bp = Blueprint('mci_health_ep', __name__)
mci_health_api = Api(mci_health_bp)
mci_health_api.add_resource(MCIHealthCheckResource, '/health/mci')
