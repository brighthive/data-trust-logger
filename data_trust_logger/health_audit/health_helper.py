import threading
import time
from datetime import datetime

import requests

from data_trust_logger.utilities import get_access_token, secure_requests


class HealthAuditThread(object):
    def __init__(self, engine, api_url, endpoints, table_to_ep_mappings={}, interval=10):
        self.engine = engine 
        self.api_url = api_url
        self.endpoints = endpoints 
        self.table_to_ep_mappings = table_to_ep_mappings
        self.interval = interval

        thread = threading.Thread(target=self.generate_endpoints_blob, args=())
        thread.daemon = True
        thread.start()


    def _get_endpoint_status(self, api_ep: str, token: str):
        try:
            response = secure_requests.secure_get(api_ep, token)
            status = response.status_code
            last_accessed = datetime.utcnow().strftime('%Y-%m-%d %H:%M')
        except Exception:
            status = 503
        
        return status, last_accessed

    def _get_endpoint_record_count(self, engine: object, endpoint: str):
        try:
            result = engine.execute(f"SELECT COUNT(*) from {endpoint}")
            count, = result.fetchone()
        except Exception:
            count = -1
        
        return count

    def generate_endpoints_blob(self):
        while True:
            endpoints_blob = {'endpoints': []}
            token = get_access_token()

            for endpoint in self.endpoints:
                try:
                    tablename = self.table_to_ep_mappings[endpoint]
                except KeyError:
                    tablename = endpoint
                
                status, last_accessed = self._get_endpoint_status(f"{self.api_url}/{endpoint}", token)
                count = self._get_endpoint_record_count(self.engine, tablename)
                
                endpoints_blob['endpoints'].append({
                    'endpoint': endpoint,
                    'record_count': count,
                    'endpoint_health': status,
                    'last_accessed': last_accessed
                })
            
            print(endpoints_blob)
            print(datetime.utcnow().strftime('%Y-%m-%d %H:%M'))
            
            time.sleep(self.interval)

    '''
    TODO: Where to save results?
    It seems like we want this data to persist, but where:

    * Save in a database. 
    * Log it (`logger.py`) – save it to a list or dict – and then pulling it from the log stream.
    * Save in memory (? – what does that mean...)
    '''
