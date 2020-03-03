from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from data_trust_logger.config import ConfigurationFactory
from data_trust_logger.health_audit.metrics_collector import \
    HealthMetricsCollector
from data_trust_logger.utilities.basic_logger import basic_logger

config = ConfigurationFactory.from_env()


def instantiate_mci_collector():
    try:
        # create_engine() itself does not establish a DB connection.
        # We call `connect()` to assess the database health early on.
        mci_engine = create_engine(config.mci_psql_uri)
        mci_engine.connect()
    except (ValueError, OperationalError) as error:
        basic_logger.error("MCI HealthMetricsCollector cannot connect to database.")
        basic_logger.error(error)
        mci_engine = None
    
    mci_tablenames = ['individual', 'source', 'gender', 'address', 'disposition', 'ethnicity_race', 'employment_status', 'education_level']
    
    return HealthMetricsCollector(
        engine=mci_engine, 
        api_url=config.mci_url,
        tablenames=mci_tablenames,
        table_to_ep_mappings=config.mci_mappings
    )
