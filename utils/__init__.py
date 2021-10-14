from utils.log import *
from utils.types import *
from utils.Utils import *

def parse_offers_to_db(offers: List[Offer]) -> List[Dict]:
    return [offer.db_parse() for offer in offers]

def get_invalid_ids_string(offers: List[Offer]) -> List[int]:
    msg = ""
    invalid_offer_ids = [offer.punk_index for offer in offers if not offer.is_valid]
    for _id in invalid_offer_ids:
        msg += f"token_ids={_id}&"
    return msg[:-1]

def parse_opensea_offers(offers: List[Dict]) -> List[Offer]:
    return offers

def parse_db_offer(offer: Dict) -> Offer:
    _offer = Offer(
        is_for_sale = offer['is_for_sale'],
        punk_index = offer['punk_index'],
        seller = offer['seller'],
        min_value = offer['min_value'],
        only_sell_to = offer['only_sell_to'],
    )
    _offer.set_ts(offer['ts'])
    return _offer

def parse_db_offers(offers: List[Dict]) -> List[Offer]:
    return [parse_db_offer(offer) for offer in offers]

def get_offer_for(punk_index: int, offers: List[Offer]) -> Offer:
    try:
        return next(offer for offer in offers if offer.punk_index == punk_index)
    except StopIteration:
        return None