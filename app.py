import os
from utils import *
from fastapi import FastAPI

app = FastAPI()
alert(f"{os.getenv('NAME')} Starting cryptopunks server now")
logger = setup_custom_logger('root')
setup_file_logger('server', logger)

@app.get("/punkfloor")
async def root():
    floor = int(redis.get(settings.REDIS_KEY_NAME))
    if floor == 0:
        alert(f"{os.getenv('NAME')} Data is not ready. Should be ready in <5 mins.")
        return {'result': 0, 'data': {'error': 'Data is not ready. Should be ready in <5 mins.'}}
    return {'result': 1, 'data': {'price': floor}}