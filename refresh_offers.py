# This script gets all offers for CryptoPunks using a web3 Wrapper and updates
# current state of offers in the database.

import gevent
from gevent import monkey
monkey.patch_all();

import settings
from utils import *

def get_web3_offers() -> List[Offer]:
    global cryptopunks
    jobs = [gevent.spawn(cryptopunks.get_offer, i) for i in settings.CRYPTO_PUNKS_RANGE]
    _ = gevent.joinall(jobs)
    return [job.value for job in jobs]

def update_offers():
    api_offers = get_web3_offers()
    db_offers = parse_db_offers(mongo.get_all_offers())
    latest_offers = []
    for punk_id in settings.CRYPTO_PUNKS_RANGE:
        api_offer = get_offer_for(punk_id, api_offers)
        db_offer = get_offer_for(punk_id, db_offers)
        if db_offer is None:
            mongo.insert_offer(api_offer.db_parse())
            latest_offers.append(api_offer)
        else:
            if api_offer.ts > db_offer.ts and not api_offer.equals(db_offer):
                alert(f"Updating offer for PUNK {punk_id} from rest program")
                mongo.update_offer(api_offer.db_parse())
                latest_offers.append(api_offer)
            else:
                latest_offers.append(db_offer)
    latest_offers = [offer for offer in latest_offers if offer.is_valid]
    latest_offers.sort(key=lambda x: x.min_value, reverse=False)
    cryptopunks.update_floor(latest_offers[0].min_value)

if __name__ == "__main__":

    logger = setup_custom_logger('root')
    setup_file_logger('refresh', logger)

    start_time = time.time()

    alert('Starting refresh offers now.')
    logger.info("Starting refresh offers now.")

    cryptopunks = Cryptopunks()
    update_offers()
    logger.info(f"Refresh offers completed in {int(time.time() - start_time)}s")
    alert(f"Refresh offers completed in {int(time.time() - start_time)}s")