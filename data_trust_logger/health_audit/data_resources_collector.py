from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from data_trust_logger.config import ConfigurationFactory
from data_trust_logger.health_audit.metrics_collector import \
    HealthMetricsCollector

config = ConfigurationFactory.from_env()

def instantiate_data_resources_collector():
    data_resources_engine = create_engine(config.dr_psql_uri)
    data_resources_url = config.dr_url
    try:
        table_names = data_resources_engine.table_names()
    except OperationalError:
        table_names = []

    metatables = ['alembic_version', 'checksums', 'logs']
    data_resources_endpoints = [endpoint for endpoint in table_names if endpoint not in metatables and "\\" not in endpoint]

    return HealthMetricsCollector(
        engine=data_resources_engine, 
        api_url=data_resources_url,
        endpoints=data_resources_endpoints
    )
