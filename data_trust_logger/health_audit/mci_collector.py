from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from data_trust_logger.config import ConfigurationFactory
from data_trust_logger.health_audit.metrics_collector import \
    HealthMetricsCollector

config = ConfigurationFactory.from_env()

def instantiate_mci_collector():
    try:
        # create_engine() itself does not establish a DB connection.
        # We call `connect()` to assess the database health early on.
        mci_engine = create_engine(config.mci_psql_uri)
        mci_engine.connect()
    except (ValueError, OperationalError):
        mci_engine = None
    
    mci_endpoints = ['users', 'source', 'gender', 'address', 'disposition', 'ethnicity', 'employment_status', 'education_level']
    table_to_ep_mappings = {
        'users': 'individual',
        'ethnicity': 'ethnicity_race',
    }

    return HealthMetricsCollector(
        engine=mci_engine, 
        api_url=config.mci_url,
        endpoints=mci_endpoints,
        table_to_ep_mappings=table_to_ep_mappings
    )
