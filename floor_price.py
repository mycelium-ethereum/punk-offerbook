import numpy as np
from utils import *
from fastapi import FastAPI

app = FastAPI()

@app.get("/punkfloor")
async def root():
    try:
        cryptopunks_offers = parse_db_offers(mongo.get_all_offers())
        cryptopunks_offers = [offer for offer in cryptopunks_offers if offer.is_valid]
        cryptopunks_offers.sort(key=lambda x: x.min_value, reverse=False)
        return {'result': 1, 'data': np.median([offer.min_value for offer in cryptopunks_offers[:4]])}
    except Exception as e:
        return {'result': 0, 'data': 'x should be greater than or equal to 1'}