"""Application Services
A collection of services for accessing external APIs.
"""

import json
import logging
import os
import sys

import requests

from data_trust_logger.config import ConfigurationFactory

config = ConfigurationFactory.from_env()
location_of_token = '/tmp/token.txt'
logger = logging.getLogger(__name__)


def get_access_token():
    """ 
    Retrieves an OAuth 2.0 access token from the OAuth 2.0 provider, and
    write the access token to a `tmp` file.
    """
    headers = {'content-type': 'application/json'}
    data = {
        'client_id': config.client_id, 
        'client_secret': config.client_secret,
        'audience': config.oauth2_audience, 
        'grant_type': 'client_credentials'
    }

    try: 
        response = requests.post(config.oauth2_url, headers=headers, data=json.dumps(data))
    except requests.exceptions.ConnectionError:
        return
    else:
        token = response.json()['access_token']
    
    with open(location_of_token, 'w+') as f:
        f.write(token)


def read_token():
    """
    Reads the access token from a temporary file, and returns the value.

    If the file does not exist, then we call `get_access_token`, and try again.
    """
    token = None

    for _ in range(2):
        try: 
            with open(location_of_token) as f:
                logger.info(f"Token read from {location_of_token}")
                token = f.read()
                break
        except FileNotFoundError as e:
            logger.error(e)
            get_access_token()
            pass
    
    return token
    

def secure_get(url: str, token: str):
    """Convenience method for GET requests against API resources.
    Args:
        url (str): The URL for the GET request.
    Returns:
        dict: Results of the query if found.
        None: If no results found.
    """
    if token:
        headers = {
            'content-type': 'application/json', 
            'authorization': 'bearer {}'.format(token)
        }

        return requests.get(url, headers=headers)
