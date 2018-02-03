import sys
import argparse
import subprocess

pools = [
    ['GarlicSoup'          , 'stratum+tcp://us.pool.garlicsoup.xyz:3333'],
    ['Bakery'              , 'stratum+tcp://pool.grlc-bakery.fun:3333'],
    ['FreshGarlicBlocks'   , 'stratum+tcp://freshgarlicblocks.net:3032'],
    ['ButterPool'          , 'stratum+tcp://butterpool.com:3032'],
    ['HappyGarlicPool'     , 'stratum+tcp://happy.garlicoin.fun:3210'],
    ['GarlicPoolOrg'       , 'stratum+tcp://stratum.garlicpool.org:3333'],
    ['GarlicMine'          , 'stratum+tcp://garlicmine.com:3333'],
    ['HRY Mining Co.'      , 'stratum+tcp://hry-mining.co:3032'],
    ['Rich Garlic Boye'    , 'stratum+tcp://rich.garlicboye.com:3333']
]

poolString = ""
i = 0
for pool in pools:
    poolString += str(i) + ": " + pool[0] + '\n'
    i += 1

parser = argparse.ArgumentParser(description='Start ccminer for a given pool or adress.')
parser.add_argument('-p', '--pool', type=int,
                   help='Index of the chosen pool (' + poolString +')')
parser.add_argument('-a', '--address',
                   help='Address to receive payouts')
parser.add_argument('-g', '--gap', type=int,
                   help='Lookup gap parameter')
args = parser.parse_args()

chosen_pool=0
if(args.pool is None):
    chosen_pool = int(input("Choose a pool:\n"+poolString))
else:
    chosen_pool = args.pool
stratum = pools[chosen_pool][1]

address = "GarLinerDG3DbH6XGEP4TGZcWrnyTbnhND"
if(args.address is not None):
    adress = args.adress

lookup_gap = 2
if(args.gap is not None):
    lookup_gap = args.gap

logfile = open('logfile', 'w')
proc=subprocess.Popen([
        'ccminer-x64',
        '-a', 'scrypt:10'
        "-L="+ str(lookup_gap), 
        "-o", stratum, 
        "-u", address
    ], 
    stdout=subprocess.PIPE, 
    stderr=subprocess.STDOUT,
    universal_newlines=True)
for line in proc.stdout:
    sys.stdout.write(line)
    logfile.write(line)
    logfile.flush()
proc.wait()