"""Data Resources Health Check API.

A simple API for returning health statistics from Data Resources.

"""
import json
import os

from flask import Blueprint, request
from flask_restful import Api, Resource
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

import data_trust_logger.utilities.responses as resp
from data_trust_logger.config import ConfigurationFactory

config = ConfigurationFactory.from_env()


class DataResourcesHealthCheckResource(Resource):
    """Health Check API."""

    def __init__(self):
        self.response = resp.ResponseBody()

    def get(self):
        metrics_data = {}
        health_audit_directory = os.path.abspath("data_trust_logger/health_audit")

        with open(f'{health_audit_directory}/metrics_blob.json') as json_data:
            metrics_data = json.load(json_data)

        return self.response.get_one_response(metrics_data)


data_resources_health_bp = Blueprint('data_resources_health_ep', __name__)
data_resources_health_api = Api(data_resources_health_bp)
data_resources_health_api.add_resource(DataResourcesHealthCheckResource, '/health/data_resources')
