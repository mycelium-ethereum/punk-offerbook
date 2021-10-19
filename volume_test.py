from utils import *

txs = parse_txs(mongo.get_transactions(timedelta(days=7)))

volume = sum(tx['value'] for tx in txs)

print(volume)