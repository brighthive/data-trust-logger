import requests

def get_endpoint_status(api_ep: str):
    try:
        response = requests.get(ap_ep)
        status = response.status_code
    except Exception:
        status = 'API error'
    
    return status

def get_endpoint_record_count(engine, endpoint: str):
    try:
        result = engine.execute(f"SELECT COUNT(*) from {endpoint}")
        count, = result.fetchone()
    except Exception:
        count = "Database error"
    
    return count