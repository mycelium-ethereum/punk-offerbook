import os
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
        mongo.update_offer(api_offer.db_parse())
    cryptopunks.update_floor(cryptopunks.get_median_of(settings.PUNKS_TO_MEDIAN))

if __name__ == "__main__":
    logger = setup_custom_logger('root')
    setup_file_logger('event', logger)

    logger.info('Starting event watcher now.')

    cryptopunks = Cryptopunks()
    for event in settings.CRYPTO_PUNKS_EVENTS:
        cryptopunks.start_streaming(event, event_handler=update_handler)

    while not cryptopunks.errored: time.sleep(1)

    alert(f"{os.getenv('NAME')} Quitting event watcher because of error - {cryptopunks.error}")
    logger.error(f"Quitting event watcher because of error - {cryptopunks.error}")
    sys.exit(1)