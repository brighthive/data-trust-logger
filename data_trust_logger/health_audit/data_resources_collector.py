from sqlalchemy.exc import OperationalError

from data_trust_logger.config import ConfigurationFactory
from data_trust_logger.health_audit.metrics_collector import \
    HealthMetricsCollector
from data_trust_logger.utilities.basic_logger import basic_logger

config = ConfigurationFactory.from_env()


def instantiate_data_resources_collector(data_resources_engine):
    try:
        # create_engine() itself does not establish a DB connection.
        # We call `connect()` to assess the database health early on.
        connection = data_resources_engine.connect()
        connection.close()
    except (ValueError, OperationalError) as error:
        basic_logger.error("Data Resources HealthMetricsCollector cannot connect to database.")
        basic_logger.error(error)
        data_resources_engine = None
        table_names = []
    else:
        # Deriving the endpoints from the database work fine, for now.
        # However, we eventually want another strategy for getting the endpoints,
        # i.e., a strategy not dependent on the database.
        table_names = data_resources_engine.table_names()

    metatables = ['alembic_version', 'checksums', 'logs']
    data_resources_tablenames = [endpoint for endpoint in table_names if endpoint not in metatables and "\\" not in endpoint]

    return HealthMetricsCollector(
        engine=data_resources_engine, 
        api_url=config.dr_url,
        tablenames=data_resources_tablenames,
        table_to_ep_mappings=config.data_resources_mappings
    )
