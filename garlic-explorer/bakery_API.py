"""
    Python scrypt to use the grlc-bakery API
    More info on https://explorer.grlc-bakery.fun/info
"""

import requests
import json

def send_request(function, parameters={}, type='api', get=1):
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
    output = nan
    if response.status_code == 200:
        # if the server responds correctly
        output = response.content
    return output    

def get_difficulty():
    """ Returns the current difficulty.
    """
    difficulty = send_request('getdifficulty')
    return double(difficulty)

def get_connectioncount():
    """ Returns the number of connections the block explorer has to other nodes.
    """
    connection_count = send_request('getconnectioncount')
    return int(connection_count)

def get_blockcount():
    """ Returns the current block index.
    """
    block_count = send_request('getblockcount')
    return int(block_count)

def get_block_hash(index):
    """ Returns the hash of the block at ; index 0 is the genesis block.
        input: block index
    """
    block_hash = send_request('getblockhash', {'index': index})
    return block_hash

def get_block(block_hash):
    """ Returns information about the block with the given hash.
        input: block hash
        ouput: block information
    """
    block = send_request('getblock', {'hash': block_hash})
    return json.loads(block)

def get_rawtransaction(txid, decrypt):
    """ Returns raw transaction representation for given transaction id. decrypt can be set to 0(false) or 1(true).
        Not working
    """
    transaction = send_request('getrawtransaction', {'txid': txid, 'decrypt': decrypt})
    return transaction

def get_networkhashps():
    """ Returns the current network hashrate. (hash/s)
    """
    hash_rate = send_request('getnetworkhashps')
    return double(hash_rate)

def get_moneysupply():
    """ Returns current money supply.
    """
    money_supply = send_request('getmoneysupply', type='ext')
    return double(money_supply)

def get_distribution():
    """ Returns wealth distribution stats.
    """
    distribution = send_request('getdistribution', type='ext')
    return json.loads(distribution)

def get_address(address_hash):
    """ Returns information for given address.
    """
    address = send_request('getaddress', address_hash, type='ext', get=0)
    return address

def get_balance(address_hash):
    """ Returns current balance of given address.
    """
    balance = send_request('getbalance', [address_hash], type='ext', get=0)
    return balance

def get_lasttxs(count, min_tx):
    """
        Returns last transactions.
        Note: returned values are in satoshis
        inputs:
            count: number of tx ton return
            min_tx: min tx to return
    """
    balance = send_request('getlasttxs', [str(count), str(min_tx)], type='ext', get=0)
    return json.loads(balance)