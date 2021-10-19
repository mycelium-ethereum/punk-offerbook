import sys
import settings
from utils import *
from client import mongo, webhook

def update_handler(event: dict):
    global cryptopunks
    event = dict(event)
    punk_index = event['args']['punkIndex']
    db_offer = parse_db_offer(mongo.get_offer(punk_index))
    api_offer = cryptopunks.get_offer(punk_index)
    if api_offer.ts > db_offer.ts and not api_offer.equals(db_offer):
        alert(f"Updating offer for PUNK {punk_index}")
        mongo.update_offer(api_offer.db_parse())

def bought_handler(event: dict):
    global cryptopunks
    update_handler(event)
    event = dict(event)
    tx_data = {
        'ts': datetime.utcnow(), 
        'hash': event['transactionHash'].hex(),
        'value': str(cryptopunks.get_tx_price(event['transactionHash'].hex()))
    }
    if not mongo.transaction_present(tx_data['hash']):
        mongo.cryptopunks_transactions.insert_one(tx_data)

if __name__ == "__main__":
    alert('Starting event watcher now.')
    logger = setup_custom_logger('root')
    setup_file_logger('event', logger)

    cryptopunks = Cryptopunks()
    for event in settings.CRYPTO_PUNKS_EVENTS:
        if event == 'PunkBought':
            cryptopunks.start_streaming(event, event_handler=bought_handler)
        else:
            cryptopunks.start_streaming(event, event_handler=update_handler)

    while not cryptopunks.errored: time.sleep(1)

    alert(f"Quitting event watcher because of error - {cryptopunks.error}")
    sys.exit(1)