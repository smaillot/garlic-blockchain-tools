from __future__ import division
from bakery_API import *
import numpy as np
import matplotlib.pylab as plt
import json
from os import listdir
from os.path import isfile, join
from time import sleep


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

def data_file_name(n_block):
    return 'data_' + str(n_block) + '.json'
    
def extract_block_number(filename):
    return int(filename.split('_')[1].split('.')[0])   

def search_transactions(addresses, start=0, end=-1, history='[]', saving=100):
    """ Read all blockchain from begining to list transactions where this address appears
    """
    def save_history(hist, block=''):
        with open('./data/' + data_file_name(block), 'w') as outfile:
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
                # print('\t\t' + str(transactions))
                print('transaction found ! (' + transactions['address'] + ': ' + transactions['value'] + ')')
                history += transactions
                
    save_history(history, end)
    return {'history': history, 'blockheight': end}
    
def plot_history(history, series={}):
    """ Plot the evolution of total coins according to time.
    """
    history = np.array(history)
    series['total'] = np.unique([t['address'] for t in history])
    
    def get_serie(addresses, history):
        hist = [t for t in history if t['address'] in addresses]
        times = [datetime.datetime.fromtimestamp(t['time']) for t in hist]
        coins = np.cumsum([t['value'] for t in hist])
        return {'times': times, 'coins': coins}
       
    ax = plt.subplot(111)
    for s in series:
        serie = get_serie(series[s], history)
        plt.plot_date(serie['times'], serie['coins'], '-', linewidth=2)
    plt.legend([s for s in series])
    
    return ax

def live_plot():
    
    datafiles = [extract_block_number(f) for f in listdir('./data') if isfile(join('./data', f)) and f.split('.')[-1] == 'json' and f.split('_')[0] == 'data']
    last = np.max(datafiles)
    last_file = data_file_name(last)
    
    with open('./data/' + last_file, 'r') as data_file:
        history = json.load(data_file)
        
    addresses = np.load('./addresses/addresses.npy')
    print('Updating history...\n\n')
    history = search_transactions(addresses, last, history=history)
    last = history['last']
    history = history['history']
    print('History up to date.')
    
    series = np.load('addresses/series')
    
    while 1:
        
        clf()
        plot_history(history, series)
        sleep(60)
        search_transactions(addresses, last, history=history)
        
if __name__ ==  '__main__':
    
    live_plot()