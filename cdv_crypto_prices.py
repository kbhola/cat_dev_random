# Get Cryptocurrency prices as a source of entropy
# Although this is tamperable and possibly predictable,
# an adviserary would have to go through a lot of trouble to replicate

import requests
import time

def get_pair_rate(pair):
    url = 'https://shapeshift.io/rate/' + str(pair)
    r = requests.get(url)
#    print(r.json())
    return r.json()

def get_market_info(pair):
    url = 'https://shapeshift.io/rate/' + str(pair)
    r = requests.get(url)
    

def shapeshift_rand_prices():
    """ Grab a tuple of BTC -> ETH, and BTC -> LTC prices to use as an entropy source
    """
    cur_pairs = ['btc_ltc', 'btc_eth']
    cur_results_raw =  map(get_pair_rate, cur_pairs)
    cur_results_rates = map(lambda x : x.get('rate'), cur_results_raw)
    cur_results = []
    for r in cur_results_rates:
        if r: # is not None
            cur_results.append(float(r))
    return bytearray(str(sum(cur_results)).encode('utf-8'))


if __name__ == '__main__':
    while True:
        print(str(shapeshift_rand_prices()))
        time.sleep(1) # delay one second
