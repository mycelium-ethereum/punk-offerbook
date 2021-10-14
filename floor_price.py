import numpy as np
from utils import *
from fastapi import FastAPI

app = FastAPI()

@app.get("/floor")
async def root():
    cryptopunks_offers = parse_db_offers(mongo.get_all_offers())
    cryptopunks_offers = [offer for offer in cryptopunks_offers if offer.is_valid]
    cryptopunks_offers.sort(key=lambda x: x.min_value, reverse=False)
    floor_price = np.median([offer.min_value for offer in cryptopunks_offers[:4]])
    return {"price": floor_price}