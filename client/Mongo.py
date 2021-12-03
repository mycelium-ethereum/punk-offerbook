import os
import ssl
import logging
from typing import List, Dict
from pymongo import MongoClient
from datetime import datetime, timedelta

class Mongo():
    def __init__(self):
        self.logger = logging.getLogger('root')
        self.client = MongoClient('mongo')
        self.cryptopunks_offerbook  = self.client.nft_offer_books.cryptopunks
        self.cryptopunks_transactions = self.client.nft_transactions.cryptopunks
        self.cryptopunks_price_history = self.client.nft_prices.cryptopunks

    def transaction_present(self, tx_hash: str) -> bool:
        return self.cryptopunks_transactions.find_one({'hash': tx_hash}) != None

    def get_transactions(self, timedelta: timedelta) -> List[Dict]:
        self.logger.info("Getting transactions...")
        return list(self.cryptopunks_transactions.find({
            'ts': {'$gte': datetime.utcnow() - timedelta}
        }))

    def get_all_offers(self) -> List[Dict]:
        self.logger.info("Getting all offers...")
        return list(self.cryptopunks_offerbook.find({}))

    def get_offer(self, punk_index: int) -> Dict:
        self.logger.info(f"Getting offer for {punk_index}...")
        return self.cryptopunks_offerbook.find_one({'punk_index': punk_index})

    def insert_offer(self, offer: Dict):
        self.logger.info(f"Inserting offer for {offer['punk_index']}...")
        self.cryptopunks_offerbook.insert_one(offer)
    
    def update_offer(self, offer: Dict):
        self.logger.info(f"Updating offer for {offer['punk_index']}...")
        self.cryptopunks_offerbook.update_one(
            {'punk_index': offer['punk_index']},
            {'$set': offer},
            upsert=False
        )

    def offer_present(self, punk_index: int) -> bool:
        return self.cryptopunks_offerbook.find_one({'punk_index': punk_index}) != None