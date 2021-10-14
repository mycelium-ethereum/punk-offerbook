from utils import *

cryptopunks_offers = parse_db_offers(mongo.get_all_offers())

# get valid offers
cryptopunks_offers = [offer for offer in cryptopunks_offers if offer.is_valid]
cryptopunks_offers.sort(key=lambda x: x.min_value, reverse=False)
print(cryptopunks_offers[:4])