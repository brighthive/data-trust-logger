"""Application Services
A collection of services for accessing external APIs.
"""

import json
import os
import sys

import requests

from data_trust_logger.config import ConfigurationFactory

config = ConfigurationFactory.from_env()


def get_access_token():
    """ Retrieves an OAuth 2.0 access token from the OAuth 2.0 provider.
    Note:
        At present, we use Auth0 as our OAuth 2.0 provider.
    Returns:
        str: OAuth 2.0 access token.
    """
    headers = {'content-type': 'application/json'}
    data = {
        'client_id': config.client_id, 
        'client_secret': config.client_secret,
        'audience': config.audience, 
        'grant_type': 'client_credentials'
    }

    try: 
        response = requests.post(config.oauth2_url, headers=headers, data=json.dumps(data))
    except requests.exceptions.ConnectionError:
        return None
    else:
        token = response.json()['access_token']
    
    return token


def secure_get(url: str, token: str):
    """Convenience method for GET requests against API resources.
    Args:
        url (str): The URL for the GET request.
    Returns:
        dict: Results of the query if found.
        None: If no results found.
    """

    # token = _get_access_token()

    if token:
        headers = {
            'content-type': 'application/json', 
            'authorization': 'bearer {}'.format(token)
        }

        return requests.get(url, headers=headers)
