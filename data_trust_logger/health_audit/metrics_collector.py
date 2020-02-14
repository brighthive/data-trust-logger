from datetime import datetime, timezone

import requests

from data_trust_logger.utilities import get_access_token, secure_requests


class HealthMetricsCollector(object):
    def __init__(self, engine, api_url, tablenames, table_to_ep_mappings={}):
        self.engine = engine 
        self.api_url = api_url
        self.tablenames = tablenames 
        self.table_to_ep_mappings = table_to_ep_mappings

    def _get_endpoint_status(self, api_ep: str, token: str):
        try:
            response = secure_requests.secure_get(api_ep, token)
            status = response.status_code
        except Exception:
            status = 503
        
        last_accessed = str(datetime.now(timezone.utc))
        
        return status, last_accessed

    def _get_endpoint_record_count(self, engine: object, endpoint: str):
        try:
            result = engine.execute(f"SELECT COUNT(*) from {endpoint}")
            count, = result.fetchone()
        except Exception:
            count = -1
        
        return count

    def collect_metrics(self):
        metrics_list = []
        token = get_access_token()

        for table in self.tablenames:
            try:
                endpoint = self.table_to_ep_mappings[table]
            except KeyError:
                endpoint = table
            
            status, last_accessed = self._get_endpoint_status(f"{self.api_url}/{endpoint}", token)
            count = self._get_endpoint_record_count(self.engine, table)
            
            metrics_list.append({
                'endpoint': endpoint,
                'record_count': count,
                'endpoint_health': status,
                'last_accessed': last_accessed
            })
        
        return metrics_list
