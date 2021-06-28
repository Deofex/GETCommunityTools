import os
import sys
import logging
import time
import logprocessor
from db.db import Database
from telegram.telegram import TelegramBot
from polgyonscan.logimporter import BlockchainLogImporter
from abidecoder.abi import decode_abi_from_url
from w3.w3 import connect_w3, load_w3contract, get_w3eventdata


# Log level 1 is INFO, Log level 2 is Debug
loglevel = int(os.environ.get('loglevel'))
polygonscanapikey = os.environ.get('polygonscanapikey')
eventscontract = os.environ.get('eventscontract')
databasename = os.environ.get('databasename')
w3url = os.environ.get('w3url')
telegramapitoken = os.environ.get('telegramapitoken')
# TODO: The ABI url below is from a proxy contract, how can this automatically be discovered?
nftcontractabiurl = 'https://api.polygonscan.com/api?module=contract&action=getabi&address=0x0230078d740b2432d7b29e4a947711cb7dd35159&format=raw'


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

# Initialize logger
logger = logging.getLogger(__name__)

logger.info('Start NFT Importer')

# Import abi functions
abifunctions = decode_abi_from_url(nftcontractabiurl)

# Initialize database
db = Database(databasename)

# Initialize Telegram bot
tg = TelegramBot(telegramapitoken,db)

# Initialize importer
bli = BlockchainLogImporter(polygonscanapikey, eventscontract)

# Initize w3 and the event contract
w3 = connect_w3(w3url)
w3eventcontract = load_w3contract(w3, eventscontract, nftcontractabiurl)

def startrun():
    fromblock = db.get_lastblock() + 1
    logs = bli.get_logs(fromblock=fromblock)

    for log in logs:
        function = abifunctions[log['topics'][0]]
        if function == 'newEventRegistered':
            eventdata = get_w3eventdata(w3eventcontract, log['topics'][1])
            logprocessor.neweventregistered(log, eventdata, db, tg)
        else:
            logger.warning('New kind of unproccessed log type found: {}'.format(
                function))


while True:
    logger.info('Start run')
    startrun()
    logger.info('End run')
    time.sleep(300)
