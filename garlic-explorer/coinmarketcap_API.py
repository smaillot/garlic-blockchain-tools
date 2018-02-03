"""
    Python scrypt to use the coinmarketcap's API
    More info on https://coinmarketcap.com/api/
"""

import requests
import json

def send_request_cmc():
    """ Sends request to coinmarketcap's API.
    """
    url = 'https://api.coinmarketcap.com/v1/ticker/garlicoin/'
    response = requests.get(url)
    output = nan
    if response.status_code == 200:
        # if the server responds correctly
        output = response.content
    return json.loads(output)