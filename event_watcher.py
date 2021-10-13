import sys
import settings
from utils.log import *
from utils.types import *
from client import mongo, webhook

logger = setup_custom_logger('root')
setup_file_logger('event', logger)

cryptopunks = Cryptopunks()
for event in settings.CRYPTO_PUNKS_EVENTS:
    cryptopunks.start_streaming(event)

while True:
    time.sleep(1)