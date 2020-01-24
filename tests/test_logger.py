"""Data Trust Logging and Health Check Unit Tests.

"""

import json
from expects import expect, be, equal, have_key


class TestLogger:
    # def test_get_data_resource_endpoints(self, client):
    #     response = client.get('/health/data_resources')
    #     body = response.json
    #     expect(response.status_code).to(be(200))
    #     expect(body).to(have_key('response'))

    def test_post_log(self, client):
        headers = {'content-type': 'application/json'}
        response = client.post('/log', headers=headers)
        expect(response.status_code).to(equal(400))
        message = {'status': 'error', 'type': 'a log thing', 'foo': 'bar'}
        response = client.post('/log', data=json.dumps(message), headers=headers)
        print(response.json)
