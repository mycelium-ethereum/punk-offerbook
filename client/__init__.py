from dotenv import load_dotenv
load_dotenv();

import os
import json
import settings
from web3 import Web3
from client.Mongo import Mongo
from client.Webhook import webhook
from client.Opensea import Opensea

def get_raw_abis(abi_paths):
    raw_abis = {}
    for abi_key, abi_path in abi_paths.items():
        with open(abi_path, "r") as f:
            raw_abis[abi_key] = json.loads(f.read())['abi']
    return raw_abis

abis = get_raw_abis(settings.ABI_PATHS)
web3 = Web3(Web3.HTTPProvider(os.environ.get("ETH_HTTP_URL")))
mongo = Mongo()
opensea = Opensea()