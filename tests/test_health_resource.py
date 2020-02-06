import json
import re

from expects import be, equal, expect, have_key, have_len
from sqlalchemy.engine import ResultProxy


def _healthcheck_response(client, metrics_blob, mocker):
    mocker.patch("json.load", return_value=metrics_blob)

    response = client.get('/health')
    expect(response.status_code).to(be(200))
    expect(response.json).to(have_key('response'))
    
    return response.json['response']

def test_mci_metrics_endpoints(client, metrics_blob, mocker):
    response = _healthcheck_response(client, metrics_blob, mocker)

    expect(response).to(have_key('mci_metrics'))
    endpoints = response['mci_metrics']
    expect(endpoints).to(have_len(2))
    
    ep_names = [ep['endpoint'] for ep in endpoints]
    expected_ep_names = ['users', 'gender']
    expect(ep_names.sort()).to(equal(expected_ep_names.sort()))

def test_data_resources_endpoints(client, metrics_blob, mocker):
    response = _healthcheck_response(client, metrics_blob, mocker)
    
    expect(response).to(have_key('data_resources_metrics'))
    endpoints = response['data_resources_metrics']
    expect(endpoints).to(have_len(1))
    
    ep_names = [ep['endpoint'] for ep in endpoints]
    expected_ep_names = ['programs']
    expect(expected_ep_names).to(equal(ep_names))
