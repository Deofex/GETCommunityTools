import os
import sys
import logging
import time
from db.db import Database
from polgyonscan.logimporter import BlockchainLogImporter
from abidecoder.abi import decode_abi_from_url
import logprocessor


# Log level 1 is INFO, Log level 2 is Debug
loglevel = int(os.environ.get('loglevel'))
polygonscanapikey = os.environ.get('polygonscanapikey')
nftcontract = os.environ.get('nftcontract')
# Database password
dbpassword = os.environ.get('POSTGRES_PASSWORD')
# TODO: The ABI url below is from a proxy contract, how can this automatically be discovered?
nftcontractabiurl = 'https://api.polygonscan.com/api?module=contract&action=getabi&address=0x4e84f3edc7be55c311162e30f3388b194e4fbdb5&format=raw'


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

# Initialize Database
db = Database(dbpassword)

# Initialize importer
bli = BlockchainLogImporter(polygonscanapikey,nftcontract)

def startrun():
    fromblock = db.get_lastblock() + 1
    logs = bli.get_logs(fromblock=fromblock)
    abifunctions = decode_abi_from_url(nftcontractabiurl)

    for log in logs:
        function = abifunctions[log['topics'][0]]
        if function == 'primarySaleMint':
            logprocessor.primarysalemint(log,db)
        elif function == 'nftMinted':
            logprocessor.nftminted(log,db)
        elif function == 'secondarySale':
            logprocessor.secondarysale(log,db)
        elif function == 'ticketInvalidated':
            logprocessor.ticketinvalidated(log,db)
        elif function == 'ticketScanned':
            logprocessor.ticketscanned(log,db)
        else:
            logger.warning('New kind of unproccessed log type found: {}'.format(
                function))

while True:
    logger.info('Start run')
    startrun()
    logger.info('End run')
    time.sleep(300)
