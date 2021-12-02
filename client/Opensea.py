import requests
from typing import List, Dict

class Opensea:
    BASE_URL = "https://api.opensea.io/wyvern/v1"
    OFFSET = 50

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        if self.api_key is not None:
            self.headers = {
                "Accept": "application/json",
                "X-API-KEY": self.api_key,
            }
        else:
            self.headers = {"Accept": "application/json"}

    def get_offers(self, address: str, id_string: str, offset: int = 0) -> List[Dict]:
        endpoint = "/orders"
        url = (
            f"{self.BASE_URL + endpoint}?asset_contract_address={address}&is_english=false"
            f"&bundled=false&include_bundled=false&include_invalid=false&{id_string}"
            f"&limit=50&offset={offset}")
        response = requests.request("GET", url, headers=self.headers)
        return response.json()['orders']

    def get_all_offers(self, address: str, id_string: str) -> List[Dict]:
        offset = 0
        offers = []
        flag = True
        while flag:
            _offers = self.get_offers(address, id_string, offset)
            offers += _offers
            if len(_offers) < self.OFFSET: flag = False
            else: offset += self.OFFSET
        return offers