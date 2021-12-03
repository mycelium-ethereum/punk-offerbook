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

def parse_db_txs(txs: List[Dict]) -> List[Dict]:
    _txs = []
    for tx in txs: 
        if tx['value'] == 'None': continue
        tx['value'] = int(tx['value'])
        _txs.append(tx)
    return _txs

def get_offer_for(punk_index: int, offers: List[Offer]) -> Offer:
    try:
        return next(offer for offer in offers if offer.punk_index == punk_index)
    except StopIteration:
        return None