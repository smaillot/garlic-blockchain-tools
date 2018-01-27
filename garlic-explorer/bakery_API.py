"""
    Python scrypt to use the grlc-bakery API
    More info on https://explorer.grlc-bakery.fun/info
"""

import requests
import json
import numpy as np

def send_request_bakery(function, parameters={}, type='api', get=1):
    """ Sends request to bakery API.
        inputs:
            function: name (ex. getdifficulty)
            parameters: parameters to send in the GET request (dict)
        output:
            response content
    """
    url = 'https://explorer.grlc-bakery.fun/' + type + '/'
    if get:
        response = requests.get(url + function, params=parameters)
    else:
        response = requests.get(url + function + '/'.join(['']+parameters), {})
    output = np.nan
    if response.status_code == 200:
        # if the server responds correctly
        output = response.content.decode('utf-8')
    return output

def extract_exchanges(dct):
    """ Extracts every addresses and value from a vin or vout dict
    """
    exchanges = [dct[i] for i in range(len(dct)) if 'scriptPubKey' in [x[0] for x in dct[i].items()]]
    if exchanges != []:
        exchanges = [[exchanges[i]['scriptPubKey']['addresses'][0], exchanges[i]['value']] for i in range(len(exchanges)) if 'addresses' in [x[0] for x in exchanges[i]['scriptPubKey'].items()]]
    return exchanges

def extract_transactions(block_hash):
    """ Returns transactions list found in a block.
    """
    transactions = [t for t in get_block(block_hash)['tx']]
    return transactions        

def get_transaction_time(txid):
    """ Returns transaction time.
    """
    return get_rawtransaction(txid)['blocktime']

def get_difficulty():
    """ Returns the current difficulty.
    """
    difficulty = send_request_bakery('getdifficulty')
    return double(difficulty)

def get_connectioncount():
    """ Returns the number of connections the block explorer has to other nodes.
    """
    connection_count = send_request_bakery('getconnectioncount')
    return int(connection_count)

def get_blockcount():
    """ Returns the current block index.
    """
    block_count = send_request_bakery('getblockcount')
    return int(block_count)

def get_block_hash(index):
    """ Returns the hash of the block at ; index 0 is the genesis block.
        input: block index
    """
    block_hash = send_request_bakery('getblockhash', {'index': index})
    return block_hash

def get_block(block_hash):
    """ Returns information about the block with the given hash.
        input: block hash
        ouput: block information
    """
    block = send_request_bakery('getblock', {'hash': block_hash})
    return json.loads(block)

def get_rawtransaction(txid):
    """ Returns raw transaction representation for given transaction id.
    """
    transaction = send_request_bakery('getrawtransaction?txid=' + txid + '&decrypt=1')
    
    if transaction != 'There was an error. Check your console.':
        # if no error
        return json.loads(transaction)
    else:
        return {}

def get_networkhashps():
    """ Returns the current network hashrate. (hash/s)
    """
    hash_rate = send_request_bakery('getnetworkhashps')
    return double(hash_rate)

def get_moneysupply():
    """ Returns current money supply.
    """
    money_supply = send_request_bakery('getmoneysupply', type='ext')
    return double(money_supply)

def get_distribution():
    """ Returns wealth distribution stats.
    """
    distribution = send_request_bakery('getdistribution', type='ext')
    return json.loads(distribution)

def get_address(address_hash):
    """ Returns information for given address.
    """
    address = send_request_bakery('getaddress', [address_hash], type='ext', get=0)
    return json.loads(address)

def get_balance(address_hash):
    """ Returns current balance of given address.
    """
    balance = send_request_bakery('getbalance', [address_hash], type='ext', get=0)
    return balance

def get_lasttxs(count, min_tx):
    """
        Returns last transactions.
        Note: returned values are in satoshis
        inputs:
            count: number of tx ton return
            min_tx: min tx to return
    """
    balance = send_request_bakery('getlasttxs', [str(count), str(min_tx)], type='ext', get=0)
    return json.loads(balance)