"""Test Fixtures"""

import pytest

from data_trust_logger import create_app


@pytest.fixture(scope='session')
def client():
    """Create a Flask Test Client.

    Returns:
        obj: A configured Flask test client.

    """
    app = create_app()
    client = app.test_client()
    return client
