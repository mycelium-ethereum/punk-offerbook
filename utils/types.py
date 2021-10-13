from __future__ import annotations
import time
import logging
import settings
from threading import Thread
from datetime import datetime
from dataclasses import dataclass
from typing import List, Callable, Dict
from client import web3, abis, webhook, mongo

class Streaming:
    def __init__(self):
        self.logger = logging.getLogger(settings.LOGGER_NAME)

    def default_handler(self, event: dict):
        self.logger.info(f"From default handler - {event}")

    def log_loop(self, event_handler: Callable, poll_interval: float = 1):
        while True:
            for event in self.event_filter.get_new_entries():
                event_handler(event)
            time.sleep(poll_interval)

    def start_streaming(self, event: str, event_handler: Callable = default_handler, **kwargs):
        self.logger.info(f"Opened stream for {event}")
        self.event_filter = self.contract.events[event].createFilter(fromBlock='latest', argument_filters=kwargs)
        thread = Thread(target=self.log_loop, args=[event_handler])
        thread.start()

class Address:
    def __init__(self, address: str, name: str = None) -> None:
        self.name = name
        self.raw = address
        self.address = self.__parse()

    def __parse(self) -> str:
        if web3.isChecksumAddress(self.raw): return self.raw
        else: return web3.toChecksumAddress(self.raw)

@dataclass
class Offer:
    is_for_sale: bool
    punk_index: int
    seller: Address
    min_value: int
    only_sell_to: Address

    def __post_init__(self):
        self.is_valid = self.is_valid_offer()

    def set_ts(self, ts: float):
        self.ts = ts
    
    def set_punk_index(self, punk_index: int):
        self.punk_index = punk_index

    def db_parse(self) -> Dict:
        return {
            'ts': self.ts, 
            'is_for_sale': self.is_for_sale,
            'punk_index': self.punk_index,
            'seller': self.seller,
            'min_value': str(self.min_value),
            'only_sell_to': self.only_sell_to,
            'is_valid': self.is_valid
        }

    def is_not_private_sale(self) -> bool:
        return self.only_sell_to == settings.NULL_ADDRESS

    def is_valid_offer(self) -> bool:
        return self.is_for_sale and self.is_not_private_sale()

    def is_equal_to(self, offer: Offer):
        return (
            self.is_for_sale == offer.is_for_sale and
            self.punk_index == offer.punk_index and 
            self.seller == offer.seller and 
            self.min_value == offer.min_value and
            self.only_sell_to == offer.only_sell_to
        )

class Cryptopunks(Streaming):
    def __init__(self):
        super().__init__()
        self.contract = web3.eth.contract(
            address=settings.CRYPTO_PUNKS_MARKET_ADDRESS,
            abi=abis['CRYPTOPUNKS']
        )

    def get_offer(self, punk_index: int) -> Offer:
        try: 
            ts = datetime.utcnow().timestamp()
            offer = Offer(*self.contract.functions.punksOfferedForSale(punk_index).call())
            offer.set_ts(ts)
            offer.set_punk_index(punk_index)
            return offer
        except Exception as e:
            print(e)
            return None

    def update_handler(self, event: dict):
        event = dict(event)
        punk_index = event['args']['punkIndex']
        db_offer = parse_db_offer(mongo.get_offer(punk_index))
        latest_offer = self.get_offer(punk_index)

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