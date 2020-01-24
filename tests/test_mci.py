import json
from expects import expect, be, equal, have_key, have_len
from sqlalchemy.engine import ResultProxy

from data_trust_logger.api.mci import MCIHealthCheckResource

def _mci_healthcheck_response(client):
    response = client.get('/health/mci')
    expect(response.status_code).to(be(200))
    expect(response.json).to(have_key('response'))
    
    return response.json['response']

def test_get_mci_endpoints(client):
    response = _mci_healthcheck_response(client)
    
    expect(response).to(have_key('endpoints'))
    endpoints = response['endpoints']
    expect(endpoints).to(have_len(8))
    
    ep_names = [ep['endpoint'] for ep in endpoints]
    expected_ep_names = MCIHealthCheckResource().endpoints
    expect(ep_names.sort()).to(be(expected_ep_names.sort()))

def test_get_mci_count(client, mocker):
    # This test mocks the behavior of the sqlalchemy engine.
    # For unit tests, these mocks enable testing the response object, without spinning up
    # a database for the MCI. Integration and E2E, however, should find an alternative strategy.
    fake_count = 4
    mocker.patch("sqlalchemy.engine.Engine.execute", return_value=ResultProxy)
    mocker.patch("sqlalchemy.engine.ResultProxy.fetchone", return_value=(fake_count,))
    
    response = _mci_healthcheck_response(client)

    expect(response).to(have_key('endpoints'))
    endpoints = response['endpoints']

    for endpoint in endpoints:
        expect(endpoint['record_count']).to(equal(fake_count))

def test_get_mci_count_fail(client, mocker):
    response = _mci_healthcheck_response(client)

    expect(response).to(have_key('endpoints'))
    endpoints = response['endpoints']

    for endpoint in endpoints:
        expect(endpoint['record_count']).to(equal('Database error'))

# TEST API endpoints (mock the endpoints...)