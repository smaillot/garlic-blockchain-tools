from __future__ import division
from bakery_API import *
import numpy as np
import matplotlib.pylab as plt
import json


def check_address_tx(addresses, tx):
    """ Search for the address in transaction tx
        input: 
            address hash
            tx: transaction hash
        output:
            amount exchanged in this transaction
    """
    transaction = get_rawtransaction(tx)
    received = {}
    
    if transaction != {}:
        
        time = transaction['blocktime']
        # check if address is a sender
            ## doesn't currently work
            # vin = transaction['vin']
            # senders = extract_exchanges(vin)
            # sent = [s[1] for s in senders if s[0] in addresses]
        
        # check if the address is a receiver
        vout = transaction['vout']
        receivers = extract_exchanges(vout)
        received = [{'time': time, 'address': r[0], 'value': r[1]} for r in receivers if r[0] in addresses]
        
    return received

def search_transactions(addresses, start=0, end=-1, history='[]', saving=100):
    """ Read all blockchain from begining to list transactions where this address appears
    """
    def save_history(hist, block=''):
        with open('data_' + str(block) + '.json', 'w') as outfile:
            json.dump(json.dumps(hist), outfile)
    
    if end == -1:
        end = get_blockcount()
        
    height = get_blockcount()
    history = json.loads(history)
    n_blocks = end - start
    for i in range(start, end):
        if np.mod(i-start, saving) == 0:
            save_history(history, i)
        print('block ' + str(i) + ' (' + str(i-start+1) + '/' + str(n_blocks) + ')')
        txs = extract_transactions(get_block_hash(i))
        n_tx = len(txs)
        for j in range(n_tx):
            print('\ttransaction ' + str(j+1) + '/' + str(n_tx))
            transactions = check_address_tx(addresses, txs[j])
            if transactions != []:
                print('\t\t' + str(transactions))
                history += transactions
                
    save_history(history, end)
    return history        
    
def plot_history(history):
    """ Plot the evolution of total coins according to time.
    """
    history = np.array(history)
    times = [datetime.datetime.fromtimestamp(t['time']) for t in history]
    coins = np.cumsum([t['value'] for t in history])
    plt.plot_date(times, coins, '-b')