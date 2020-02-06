"""Test Fixtures"""

import json
import os

import pytest

from data_trust_logger import create_app


@pytest.fixture
def metrics_blob():
    test_directory = os.path.abspath(os.path.dirname(__file__))
    with open(f'{test_directory}/metrics_blob.test.json') as json_data:
        return json.load(json_data)

@pytest.fixture(scope='session')
def client():
    """Create a Flask Test Client.

    Returns:
        obj: A configured Flask test client.

    """
    app = create_app()
    client = app.test_client()
    return client
