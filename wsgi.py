import os
from data_trust_logger import create_app
environment = os.getenv('APP_ENV', None)

app = application = create_app(environment)