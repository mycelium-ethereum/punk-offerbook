# This script gets all offers for CryptoPunks using a web3 Wrapper and updates
# current state of offers in the database.

import gevent
from gevent import monkey
monkey.patch_all();

import sys
import settings
from utils.log import *
from utils.types import *
from client import mongo, webhook

def get_web3_offers() -> List[Offer]:
    global cryptopunks
    jobs = [gevent.spawn(cryptopunks.get_offer, i) for i in settings.CRYPTO_PUNKS_RANGE]
    _ = gevent.joinall(jobs)
    return [job.value for job in jobs]

def update_offers(first_run: bool = False):
    api_offers = get_web3_offers()

    if first_run: 
        _api_offers = [offer.db_parse() for offer in api_offers]
        mongo.cryptopunks_offerbook.insert_many(_api_offers)
        return

    db_offers = parse_db_offers(mongo.get_all_offers())
    for punk_id in settings.CRYPTO_PUNKS_RANGE:
        api_offer = get_offer_for(punk_id, api_offers)
        db_offer = get_offer_for(punk_id, db_offers)
        if db_offer is None:
            mongo.insert_offer(api_offer.db_parse())
        else:
            earliest_offer = api_offer if api_offer.ts > db_offer.ts else db_offer
            if not api_offer.is_equal_to(earliest_offer):
                webhook.send(f"Updating offer for PUNK {punk_id} from rest program")
                mongo.update_offer(earliest_offer.db_parse())

if __name__ == "__main__":
    logger = setup_custom_logger('root')
    setup_file_logger('refresh', logger)

    try: 
        first_run = sys.argv[1]
        first_run = True
    except: 
        first_run = False

    cryptopunks = Cryptopunks()
    update_offers(first_run)