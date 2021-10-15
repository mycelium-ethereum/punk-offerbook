import numpy as np
from utils import *
from fastapi import FastAPI

app = FastAPI()

@app.get("/punkfloor")
async def root(x: int):
    if x >= 1:
        cryptopunks_offers = parse_db_offers(mongo.get_all_offers())
        cryptopunks_offers = [offer for offer in cryptopunks_offers if offer.is_valid]
        cryptopunks_offers.sort(key=lambda x: x.min_value, reverse=False)
        return {'result': 1, 'data': cryptopunks_offers[x-1]}
    return {'result': 0}