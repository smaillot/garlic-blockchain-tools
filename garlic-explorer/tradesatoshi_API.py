"""
    Python scrypt to use the tradesatoshi's API
    More info on https://tradesatoshi.com/Home/Api
"""

import requests
import json

def send_request_ts(function, parameters={}, type='public'):
    """ Sends request to tradesatoshi' API.
        inputs:
            function: name (ex. getdifficulty)
            parameters: parameters to send in the GET request (dict)
        output:
            response content
    """
    url = 'https://tradesatoshi.com/Home/Api'
    
    response = requests.get(url + type + function, params=parameters)    
    output = np.nan
    
    if response.status_code == 200:
        # if the server responds correctly
        output = response.content.decode('utf-8')
        
    return output

def get_currencies():
    
    currencies = send_request_ts('GetCurrencies')
    
    try:
        currencies = json.loads(currencies)
    except:
        currencies = {}
        
    return currencies

 def get_ticker(market):
     
     ticker = send_request_ts('GetTicker', {'market': maket})
    
    try:
        ticker = json.loads(ticker)
    except:
        ticker = {}
        
    return ticker

def get_market_history(market, count):
     
     history = send_request_ts('GetMarketHistory', {'market': maket, 'count': count})
    
    try:
        history = json.loads(history)
    except:
        history = {}
        
    return history

def get_market_summary(market):
     
     summary = send_request_ts('GetMarketSummary', {'market': maket})
    
    try:
        summary = json.loads(summary)
    except:
        summary = {}
        
    return summary

def get_market_summaries():
     
     summaries = send_request_ts('GetMarketSummaries')
    
    try:
        summaries = json.loads(summaries)
    except:
        summaries = {}
        
    return summaries

def get_orderbook(market, type, depth):
     
     orderbook = send_request_ts('GetOrderBook', {'market': market, 'type': type, 'depth', depth})
    
    try:
        orderbook = json.loads(orderbook)
    except:
        orderbook = {}
        
    return orderbook