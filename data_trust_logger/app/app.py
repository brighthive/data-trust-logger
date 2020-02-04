"""Data Trust Logger Application."""

from flask import Flask
from flask_cors import CORS

from data_trust_logger.api import mci_health_bp, data_resources_health_bp, log_bp


# Health thread stuff...
from data_trust_logger.health_audit.health_helper import HealthAuditThread
from data_trust_logger.config import ConfigurationFactory
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
config = ConfigurationFactory.from_env()
engine = create_engine(config.mci_psql_uri)
endpoints = ['users', 'source', 'gender', 'address', 'disposition', 'ethnicity', 'employment_status', 'education_level']
table_to_ep_mappings = {
    'users': 'individual',
    'ethnicity': 'ethnicity_race',
}


def create_app(environment: str = None):
    """Create the Flask application.

    Returns:
        obj: The configured Flask application context

    """

    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(mci_health_bp)
    app.register_blueprint(data_resources_health_bp)
    app.register_blueprint(log_bp)
    
    # We'll have a thread with each gunicorn worker – is that too many threads?
    # Where else could this live? 
    # In an executable script that gets run in `cmd.sh`. This entails adding a setup.py file (I think).

    # Should we instantiate a different threaded process for MCI vs. DR API? Or should the
    #  the HealthAuditThread handle both?
    HealthAuditThread(engine=engine, api_url=config.mci_url, endpoints=endpoints, table_to_ep_mappings=table_to_ep_mappings)

    return app
