import logging

# Logging settings
LOG_LEVEL = logging.DEBUG
CONSOLE_LOG_LEVEL = logging.DEBUG
FILE_LOG_LEVEL = logging.DEBUG
LOGGER_NAME = 'root'

# ABI settings
ABI_PATHS = {'CRYPTOPUNKS': 'abis/CryptoPunksMarket.json'}

# Etherscan settings
TXS_PER_RESPONSE = 10000

# Ethereum settings
NULL_ADDRESS = "0x0000000000000000000000000000000000000000"
AVERAGE_BLOCK_TIME = 15 # in seconds

# Cryptopunks
CRYPTO_PUNKS_RANGE = range(10000)
CRYPTO_PUNKS_MARKET_ADDRESS = "0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB"
WRAPPED_PUNKS_ADDRESS = "0xb7f7f6c52f2e2fdb1963eab30438024864c313f6"

CRYPTO_PUNKS_EVENTS = [
    'PunkTransfer',
    'PunkOffered',
    'PunkBidEntered',
    'PunkBidWithdrawn',
    'PunkBought',
    'PunkNoLongerForSale'
]