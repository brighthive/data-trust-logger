"""Data Trust Logging and Health Check Unit Tests.

"""

import json
from expects import expect, be, equal, have_key


class TestLogger:
    def test_log_empty_body(self, client, mocker):
        mocker.patch('brighthive_authlib.providers.BrightHiveProvider.validate_token', return_value=True)
        headers = {'content-type': 'application/json'}
        response = client.post('/log', headers=headers)

        expect(response.status_code).to(equal(400))
        expect(response.json['messages']).to(equal(['Empty request body.']))
    
    def test_log_with_data(self, client, mocker):
        mocker.patch('brighthive_authlib.providers.BrightHiveProvider.validate_token', return_value=True)
        headers = {'content-type': 'application/json'}
        message = {'status': 'error', 'type': 'a log thing', 'foo': 'bar'}
        response = client.post('/log', data=json.dumps(message), headers=headers)

        expect(response.status_code).to(equal(201))
        expect(response.json['messages']).to(equal(['Successfully logged message']))
