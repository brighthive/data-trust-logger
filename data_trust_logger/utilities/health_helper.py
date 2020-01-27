from datetime import datetime

import requests

from data_trust_logger.utilities import secure_requests


def _get_endpoint_status(api_ep: str):
    try:
        response = secure_requests.secure_get(api_ep)
        status = response.status_code
        last_accessed = datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    except Exception:
        status = 503
    
    return status, last_accessed

def _get_endpoint_record_count(engine: object, endpoint: str):
    try:
        result = engine.execute(f"SELECT COUNT(*) from {endpoint}")
        count, = result.fetchone()
    except Exception:
        count = -1
    
    return count

def generate_endpoints_blob(engine: object, api_url: str, endpoints: list, mappings={}):
    endpoints_blob = {'endpoints': []}
    for endpoint in endpoints:
        try:
            tablename = mappings[endpoint]
        except KeyError:
            tablename = endpoint
        
        status, last_accessed = _get_endpoint_status(f"{api_url}/{endpoint}")
        count = _get_endpoint_record_count(engine, tablename)
        
        endpoints_blob['endpoints'].append({
            'endpoint': endpoint,
            'record_count': count,
            'endpoint_health': status,
            'last_accessed': last_accessed
        })
    
    return endpoints_blob
