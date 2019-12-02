"""Generate fake API health statistics.

Generates fake API health statistics for testing.

"""

import random
from collections import OrderedDict
from datetime import datetime


def _get_fake_health():
    health_status = ['healthy', 'unhealthy']
    return health_status[random.randint(0, 1)]


def _get_fake_call_count():
    return random.randint(0, 100000)


def generate_fake_results(endpoint_list: list):
    endpoints = {'endpoints': []}
    if len(endpoint_list) > 0:
        for endpoint in endpoint_list:
            endpoints['endpoints'].append({
                'endpoint': endpoint,
                'status': _get_fake_health(),
                '30_day_call_count': _get_fake_call_count(),
                'last_accessed': datetime.utcnow().strftime('%Y-%m-%d %H:%M')
            })
    return endpoints
