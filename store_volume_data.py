import os
import requests
import settings
from utils import *

def get_transactions(days_ago: int) -> List[Dict]:
    current_block = web3.eth.get_block('latest').number
    estimated_blocks_ago = days_ago * 24 * 60 * 60 / settings.AVERAGE_BLOCK_TIME
    start_block = current_block - estimated_blocks_ago
    url = (
        "https://api.etherscan.io/api?module=account&action=txlist"
        f"&address={settings.CRYPTO_PUNKS_MARKET_ADDRESS}"
        f"&startblock={start_block}&endblock={current_block}"
        f"&page=1&sort=desc&apikey={os.getenv('ETHERSCAN_KEY')}"
    )
    return requests.get(url).json()['result']

def parse_txs(txs: List[Dict]) -> List[Dict]:
    global cryptopunks
    _txs_to_return = []
    for tx in txs:
        try: func, params = cryptopunks.contract.decode_function_input(tx['input'])
        except: func, params = None, None
        if str(func) == "<Function acceptBidForPunk(uint256,uint256)>":
            _txs_to_return.append({
                'ts': datetime.utcfromtimestamp(int(tx['timeStamp'])),
                'hash': tx['hash'],
                'value': str(params['minPrice']),
            })
        elif str(func) == "<Function buyPunk(uint256)>":
            _txs_to_return.append({
                'ts': datetime.utcfromtimestamp(int(tx['timeStamp'])),
                'hash': tx['hash'],
                'value': str(tx['value']),
            })
    return _txs_to_return

if __name__ == "__main__":
    cryptopunks = Cryptopunks()
    raw_txs = get_transactions(days_ago=7)
    txs = parse_txs(raw_txs)
    for tx in txs:
        if not mongo.transaction_present(tx['hash']):
            mongo.cryptopunks_transactions.insert_one(tx)