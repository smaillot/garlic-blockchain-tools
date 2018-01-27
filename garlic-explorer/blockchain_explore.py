import bakery_API


def check_address_tx(address, tx):
    """ Search for the address in transaction tx
        input: 
            address hash
            tx: transaction hash
        output:
            amount exchanged in this transaction
    """
    transaction = get_rawtransaction(tx)
    
    if transaction != {}:
        ## Search only in receivers for counting mining only
            # check if address is a sender
            #vin = transaction['vin']
            #senders = extract_exchanges(vin)
            #sent = [s[1] for s in senders if s[0] == address]
        
        # check if the address is a receiver
        vout = transaction['vout']
        receivers = extract_exchanges(vout)
        received = [r[1] for r in receivers if r[0] == address]
        
        amount = sum(received) # - sum(sent)
    else:
        amount = 0
        
    return amount

def check_all_transactions(address, start=0, end=-1):
    """ Read all blockchain from begining to list transactions where this address appears
    """
    if end == -1:
        end = get_blockcount()
    height = get_blockcount()
    hist = []
    for i in range(start, end):
        print(i)
        txs = extract_transactions(get_block_hash(i))
        for tx in txs:
            amount = check_address_tx(address, tx)
            if amount != 0:
                transaction = [get_transaction_time(tx), amount]
                print(transaction)
                hist.append(transaction)
    return hist        
    