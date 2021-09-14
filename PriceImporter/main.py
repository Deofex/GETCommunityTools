import os
import sys
import logging
import requests
import json
import time
from db.db import Database



# Log level 1 is INFO, Log level 2 is Debug
loglevel = int(os.environ.get('loglevel'))
# Database password
dbpassword = os.environ.get('POSTGRES_PASSWORD')


# Configure the logger
if loglevel == 1:
    loglevel = logging.INFO
elif loglevel == 2:
    loglevel = logging.DEBUG
logging.basicConfig(
    format=('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
    datefmt="%a %d/%m/%Y %H:%M:%S",
    level=loglevel,
    stream=sys.stdout)

def get_url(url, headers=None):
    '''Retrieve content from an URL'''
    response = requests.get(url, headers=headers)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url, headers=None):
    '''Retrieve a JSON file from an URL'''
    content = get_url(url, headers)
    js = json.loads(content)
    return js

def get_getprice():
    url = ('https://api.coingecko.com/api/v3/coins/ethereum/contract/'
        '0x8a854288a5976036a725879164ca3e91d30c6a1b')
    r = get_json_from_url(url)
    price = r['market_data']['current_price']['eur']
    logger.info('The current GET price is: {}'.format(price))
    return price


# Initialize logger
logger = logging.getLogger(__name__)

logger.info('Start Price Importer')

# Initialize Database
db = Database(dbpassword)

price = db.get_price('GET')

if price == None:
    logger.info('There''s no price available, collect price and store it')
    getprice = get_getprice()
    db.create_price('GET',getprice)
else:
    logger.info('Stored GET price is: {}'.format(price))

# Keep updating the price every 10 minutes
while True:
    logger.info('Start updating price cycle')
    getprice = get_getprice()
    db.update_price('GET', getprice)
    # Sleep 10 minutes
    time.sleep(600)


