import json
import re

import requests_mock
from expects import be, equal, expect, have_key, have_len
from sqlalchemy.engine import ResultProxy


def _data_resources_healthcheck_response(client, mocker):
    mocker.patch("sqlalchemy.engine.Engine.table_names", return_value=["programs", "credentials", "checksums", "alembic_version"])

    response = client.get('/health/data_resources')
    expect(response.status_code).to(be(200))
    expect(response.json).to(have_key('response'))
    
    return response.json['response']

def test_get_data_resources_endpoints(client, mocker):
    response = _data_resources_healthcheck_response(client, mocker)
    
    expect(response).to(have_key('endpoints'))
    endpoints = response['endpoints']
    expect(endpoints).to(have_len(2))
    
    ep_names = [ep['endpoint'] for ep in endpoints]
    expected_ep_names = ['programs', 'credentials']
    expect(ep_names.sort()).to(be(expected_ep_names.sort()))

def test_get_data_resources_count(client, mocker):
    # This test mocks the behavior of the sqlalchemy engine.
    # For unit tests, these mocks enable testing the response object, without spinning up
    # a database for the MCI. Integration and E2E, however, should find an alternative strategy.
    fake_count = 4
    mocker.patch("sqlalchemy.engine.Engine.execute", return_value=ResultProxy)
    mocker.patch("sqlalchemy.engine.ResultProxy.fetchone", return_value=(fake_count,))
    
    response = _data_resources_healthcheck_response(client, mocker)

    expect(response).to(have_key('endpoints'))
    endpoints = response['endpoints']

    for endpoint in endpoints:
        expect(endpoint['record_count']).to(equal(fake_count))

def test_get_data_resources_count_fail(client, mocker):
    response = _data_resources_healthcheck_response(client, mocker)

    expect(response).to(have_key('endpoints'))
    endpoints = response['endpoints']

    for endpoint in endpoints:
        expect(endpoint['record_count']).to(equal('Database error'))

def test_get_data_resources_statuses(client, mocker):
    with requests_mock.Mocker() as m:
        matcher = re.compile('/programs')
        m.get(matcher, json={}, status_code=200)
        m.post("https://brighthive-test.auth0.com/oauth/token", json={"access_token": "123456"}, status_code=201)
        response = _data_resources_healthcheck_response(client, mocker)

    expect(response).to(have_key('endpoints'))
    endpoints = response['endpoints']

    for endpoint in endpoints:
        if endpoint['endpoint'] == 'programs':
            expect(endpoint['endpoint_health']).to(equal(200))
        else:
            expect(endpoint['endpoint_health']).to(equal('API error'))
