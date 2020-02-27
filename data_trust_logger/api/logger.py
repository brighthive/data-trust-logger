"""Logging API.

A simple API for passing log output to standard out for downstream processing. The goal of this utility
is to enable web applications (such as Facet) to have a means of providing output to the data trust infrastructure.

"""

import json
import logging
import sys

from brighthive_authlib import token_required
from flask import Blueprint, request
from flask_restful import Api, Resource

import data_trust_logger.utilities.responses as resp
from data_trust_logger.config import ConfigurationFactory

config = ConfigurationFactory.from_env()


class LogResource(Resource):
    """Log API."""

    def __init__(self):
        self.response = resp.ResponseBody()
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)
        log_handler = logging.StreamHandler(sys.stdout)
        log_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        log_handler.setFormatter(formatter)

        self.log.addHandler(log_handler)

    @token_required(config.oauth2_provider)
    def post(self):
        try:
            data = request.get_json(force=True)
            self.log.info(json.dumps(data))
        except Exception as e:  
            return self.response.empty_request_body_response()

        return self.response.custom_response(status='OK', code=201, messages=['Successfully logged message'])


log_bp = Blueprint('log_ep', __name__)
log_api = Api(log_bp)
log_api.add_resource(LogResource, '/log')
