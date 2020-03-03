import re
from unittest.mock import mock_open

from expects import be, equal, expect, have_key, have_len

from data_trust_logger.health_audit.mci_collector import \
    instantiate_mci_collector


def test_get_statuses_with_invalid_token(client, mocker):
    """
    Test that endpoints return a 401 status code when `/tmp/token.txt` does not contain a valid token.
    """
    mocker.patch('data_trust_logger.utilities.secure_requests.open', mock_open(read_data='invalid token'))
    collector = instantiate_mci_collector()
    metrics = collector.collect_metrics()

    for entry in metrics:
        expect(entry['endpoint_health']).to(equal(401))
