import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from data_trust_logger.config import ConfigurationFactory
from data_trust_logger.health_audit.metrics_collector import \
    HealthMetricsCollector

config = ConfigurationFactory.from_env()
logger = logging.getLogger(__name__)


def instantiate_data_resources_collector():
    try:
        # create_engine() itself does not establish a DB connection.
        # We call `connect()` to assess the database health early on.
        data_resources_engine = create_engine(config.dr_psql_uri)
        data_resources_engine.connect()
    except (ValueError, OperationalError) as error:
        logger.error("Data Resources HealthMetricsCollector cannot connect to database.")
        logger.error(error)
        data_resources_engine = None
        table_names = []
    else:
        # Deriving the endpoints from the database work fine, for now.
        # However, we eventually want another strategy for getting the endpoints,
        # i.e., a strategy not dependent on the database.
        table_names = data_resources_engine.table_names()

    metatables = ['alembic_version', 'checksums', 'logs']
    data_resources_endpoints = [endpoint for endpoint in table_names if endpoint not in metatables and "\\" not in endpoint]

    return HealthMetricsCollector(
        engine=data_resources_engine, 
        api_url=config.dr_url,
        endpoints=data_resources_endpoints
    )
