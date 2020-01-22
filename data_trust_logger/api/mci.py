"""MCI Health Check API.

A simple API for returning health statistics from MCI.

"""

from flask import Blueprint, request
from flask_restful import Api, Resource
from sqlalchemy import MetaData, Table, create_engine

import data_trust_logger.utilities.fake_results as fake
import data_trust_logger.utilities.responses as resp
from data_trust_logger.config import ConfigurationFactory

config = ConfigurationFactory.from_env()


class MCIHealthCheckResource(Resource):
    """Health Check API."""

    def __init__(self):
        self.response = resp.ResponseBody()
        self.endpoints = ['/mci/users', '/mci/source', '/mci/gender', '/mci/address', '/mci/disposition', '/mci/ethnicity',
                          '/mci/employment_status', '/mci/education_level']

    def get(self):
        engine = create_engine(config.MCI_DATABASE_URI)
        metadata = MetaData(bind=engine)

        # TODO: Dynamically do this for each endpoint. (N.b., might need a special case for `users`/Individual)
        individual = Table('individual', metadata, autoload=True)
        results = engine.execute(individual.count())
        count = results.first()[0]   

        return self.response.get_one_response(fake.generate_fake_results(self.endpoints))


mci_health_bp = Blueprint('mci_health_ep', __name__)
mci_health_api = Api(mci_health_bp)
mci_health_api.add_resource(MCIHealthCheckResource, '/health/mci')
