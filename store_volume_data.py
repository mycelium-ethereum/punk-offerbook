import os
import requests
import settings
from utils import *

def get_transactions(days_ago: int) -> List[Dict]:
    current_block = web3.eth.get_block('latest').number
    estimated_blocks_ago = days_ago * 24 * 60 * 60 / settings.AVERAGE_BLOCK_TIME
    start_block = current_block - estimated_blocks_ago
    url = (
        "https://api.etherscan.io/api?module=account&action=txlist"
        f"&address={settings.CRYPTO_PUNKS_MARKET_ADDRESS}"
        f"&startblock={start_block}&endblock={current_block}"
        f"&page=1&offset=10&sort=asc&apikey={os.getenv('ETHERSCAN_KEY')}"
    )
    return requests.get(url)

response = get_transactions(days_ago=7)
print(response.json()['result'])