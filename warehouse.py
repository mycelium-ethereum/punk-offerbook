import requests
from datetime import datetime
from scraper import CryptopunksScraper
from utils import mongo, setup_file_logger, setup_custom_logger

if __name__ == "__main__":

    logger = setup_custom_logger('root')
    setup_file_logger('historical_prices', logger)
    ts_now = datetime.utcnow()

    try:
        cryptopunks_scraper = CryptopunksScraper()
        scraper_floor = cryptopunks_scraper.get_floor_price()
    except Exception as e:
        scraper_floor = 0
        logger.error(f"Error {e} while getting cryptopunks floor price from scraper.")
    
    try:
        ea_floor = requests.get('http://35.225.49.140:3400/punkfloor').json()['data']['price'] / 10**18
    except Exception as e:
        ea_floor = 0
        logger.error(f"Error {e} while getting cryptopunks floor price from external adapter.")

    mongo.cryptopunks_price_history.insert_one({
        'ts': ts_now,
        'ea_floor': ea_floor,
        'scraper_floor': scraper_floor,
    })
    