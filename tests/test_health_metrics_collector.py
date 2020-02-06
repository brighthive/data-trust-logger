import json
import re

import requests_mock
from expects import be, equal, expect, have_key, have_len
from sqlalchemy.engine import ResultProxy, Engine

from data_trust_logger.health_audit.mci_collector import instantiate_mci_collector
from data_trust_logger.health_audit.data_resources_collector import instantiate_data_resources_collector


def test_get_mci_count(mocker):
    # This test mocks the behavior of the sqlalchemy engine.
    # For unit tests, these mocks enable testing the response object, without spinning up
    # a database for the MCI. Integration and E2E, however, should find an alternative strategy.
    seeded_count = 4
    mocker.patch("sqlalchemy.create_engine", return_value=Engine)
    mocker.patch("sqlalchemy.engine.Engine.connect", return_value=True)
    mocker.patch("sqlalchemy.engine.Engine.execute", return_value=ResultProxy)
    mocker.patch("sqlalchemy.engine.ResultProxy.fetchone", return_value=(seeded_count,))
    
    collector = instantiate_mci_collector()
    metrics = collector.collect_metrics()

    record_counts = [entry["record_count"] for entry in metrics]

    for count in record_counts:
        assert count == seeded_count

def test_get_mci_count_fail():
    collector = instantiate_mci_collector()
    metrics = collector.collect_metrics()

    record_counts = [entry["record_count"] for entry in metrics]

    for count in record_counts:
        assert count == -1

def test_get_mci_statuses(client):
    with requests_mock.Mocker() as m:
        matcher = re.compile('/gender')
        m.get(matcher, json={}, status_code=200)
        m.post("https://brighthive-test.auth0.com/oauth/token", json={"access_token": "123456"}, status_code=201)

        collector = instantiate_mci_collector()
        metrics = collector.collect_metrics()

    for entry in metrics:
        if entry['endpoint'] == 'gender':
            expect(entry['endpoint_health']).to(equal(200))
        else:
            expect(entry['endpoint_health']).to(equal(503))

def test_get_data_resources_count(mocker):
    # This test mocks the behavior of the sqlalchemy engine.
    # For unit tests, these mocks enable testing the response object, without spinning up
    # a database for the DR API. Integration and E2E, however, should find an alternative strategy.
    seeded_count = 4
    mocker.patch("sqlalchemy.create_engine", return_value=Engine)
    mocker.patch("sqlalchemy.engine.Engine.connect", return_value=True)
    mocker.patch("sqlalchemy.engine.Engine.table_names", return_value=["programs", "credentials", "checksums", "alembic_version"])
    mocker.patch("sqlalchemy.engine.Engine.execute", return_value=ResultProxy)
    mocker.patch("sqlalchemy.engine.ResultProxy.fetchone", return_value=(seeded_count,))
    
    collector = instantiate_data_resources_collector()
    metrics = collector.collect_metrics()

    record_counts = [entry["record_count"] for entry in metrics]

    for count in record_counts:
        assert count == seeded_count

def test_get_mci_count_fail():
    collector = instantiate_data_resources_collector()
    metrics = collector.collect_metrics()

    record_counts = [entry["record_count"] for entry in metrics]

    for count in record_counts:
        assert count == -1

def test_get_mci_statuses(client):
    with requests_mock.Mocker() as m:
        matcher = re.compile('/programs')
        m.get(matcher, json={}, status_code=200)
        m.post("https://brighthive-test.auth0.com/oauth/token", json={"access_token": "123456"}, status_code=201)

        collector = instantiate_data_resources_collector()
        metrics = collector.collect_metrics()

    for entry in metrics:
        if entry['endpoint'] == 'programs':
            expect(entry['endpoint_health']).to(equal(200))
        else:
            expect(entry['endpoint_health']).to(equal(503))
