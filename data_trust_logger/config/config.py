import os

class Config(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        os.environ['FLASK_ENV'] = 'development'

    DEBUG = True

    MCI_PSQL_USER = 'brighthive'
    MCI_PSQL_PASSWORD = 'test_password'
    MCI_PSQL_DATABASE = 'mci_dev'
    MCI_PSQL_PORT = '5432'
    MCI_PSQL_HOSTNAME = 'localhost' 
    # MCI_PSQL_HOSTNAME = 'docker_postgres_mci_1'
    # If the Logger API is running in a Docker container, then connect to the 
    # mci psql container, rather than localhost. 
    MCI_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        MCI_PSQL_USER,
        MCI_PSQL_PASSWORD,
        MCI_PSQL_HOSTNAME,
        MCI_PSQL_PORT,
        MCI_PSQL_DATABASE
    )

class ConfigurationFactory(object):
    @staticmethod
    def get_config(config_type: str):
        """Return a configuration by it's type.
        Primary factory method that returns a configuration object based on the provided configuration type.
        Args:
            config_type (str): Configuration factory type return. May be one of:
                - TEST
                - DEVELOPMENT
                - INTEGRATION
                - SANDBOX
                - PRODUCTION
        Returns:
            object: Configuration object based on the specified config_type.
        """
        if config_type.upper() == 'DEVELOPMENT':
            return DevelopmentConfig()
        elif config_type.upper() == 'TEST':
            return TestConfig()

    @staticmethod
    def from_env():
        """Retrieve configuration based on environment settings.
        Provides a configuration object based on the settings found in the `APP_ENV` variable. Defaults to the `development`
        environment if the variable is not set.
        Returns:
            object: Configuration object based on the configuration environment found in the `APP_ENV` environment variable.
        """
        environment = os.getenv('APP_ENV', 'DEVELOPMENT')

        return ConfigurationFactory.get_config(environment)