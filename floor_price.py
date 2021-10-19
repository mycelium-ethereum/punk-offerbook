from utils import *
from fastapi import FastAPI

app = FastAPI()

@app.get("/punkfloor")
async def root():
    try:
        cryptopunks_offers = parse_db_offers(mongo.get_all_offers())
        if len(cryptopunks_offers) != 10000:
            return {'result': 0, 'data': {'error': 'Data is not ready. Should be ready in <1 hr.'}}
        cryptopunks_offers = [offer for offer in cryptopunks_offers if offer.is_valid]
        cryptopunks_offers.sort(key=lambda x: x.min_value, reverse=False)
        return {'result': 1, 'data': {'price': cryptopunks_offers[0].min_value}}
    except Exception as e:
        return {'result': 0, 'data': {'error': 'x should be greater than or equal to 1'}}