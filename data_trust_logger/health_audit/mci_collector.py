from sqlalchemy import create_engine

from data_trust_logger.config import ConfigurationFactory
from data_trust_logger.health_audit.metrics_collector import \
    HealthMetricsCollector

config = ConfigurationFactory.from_env()

def instantiate_mci_collector():
    mci_engine = create_engine(config.mci_psql_uri)
    mci_url = config.mci_url
    mci_endpoints = ['users', 'source', 'gender', 'address', 'disposition', 'ethnicity', 'employment_status', 'education_level']
    table_to_ep_mappings = {
        'users': 'individual',
        'ethnicity': 'ethnicity_race',
    }

    return HealthMetricsCollector(
        engine=mci_engine, 
        api_url=mci_url,
        endpoints=mci_endpoints,
        table_to_ep_mappings=table_to_ep_mappings
    )
