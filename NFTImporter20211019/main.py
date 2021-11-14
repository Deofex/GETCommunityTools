import os
import sys
import logging
import time
from db.db import Database
from infura.infura import Infura
import logprocessor


# Log level 1 is INFO, Log level 2 is Debug
loglevel = int(os.environ.get('loglevel'))
w3url = os.environ.get('w3url')
nftcontract = os.environ.get('nftcontract20211019')
# Database password
dbpassword = os.environ.get('POSTGRES_PASSWORD')
# The contract ABI
nftabi = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"nftIndex","type":"uint256"},{"indexed":true,"internalType":"uint64","name":"getUsed","type":"uint64"},{"indexed":true,"internalType":"uint64","name":"orderTime","type":"uint64"}],"name":"CheckedIn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"nftIndex","type":"uint256"},{"indexed":true,"internalType":"uint64","name":"getUsed","type":"uint64"},{"indexed":true,"internalType":"uint64","name":"orderTime","type":"uint64"},{"indexed":false,"internalType":"uint256","name":"basePrice","type":"uint256"}],"name":"CollateralizedMint","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"stateOfSwitch","type":"bool"},{"indexed":false,"internalType":"uint256","name":"refactorSwapIndex","type":"uint256"}],"name":"EconomicsFlipped","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"nftIndex","type":"uint256"},{"indexed":true,"internalType":"uint64","name":"getUsed","type":"uint64"},{"indexed":true,"internalType":"uint64","name":"orderTime","type":"uint64"}],"name":"IllegalCheckIn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"nftIndex","type":"uint256"},{"indexed":true,"internalType":"uint64","name":"getUsed","type":"uint64"},{"indexed":true,"internalType":"uint64","name":"orderTime","type":"uint64"}],"name":"IllegalScan","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"nftIndex","type":"uint256"},{"indexed":true,"internalType":"uint64","name":"getUsed","type":"uint64"},{"indexed":true,"internalType":"uint64","name":"orderTime","type":"uint64"}],"name":"NftClaimed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"nftIndex","type":"uint256"},{"indexed":true,"internalType":"uint64","name":"getUsed","type":"uint64"},{"indexed":true,"internalType":"uint64","name":"orderTime","type":"uint64"},{"indexed":false,"internalType":"uint256","name":"basePrice","type":"uint256"}],"name":"PrimarySaleMint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"nftIndex","type":"uint256"},{"indexed":true,"internalType":"uint64","name":"getUsed","type":"uint64"},{"indexed":true,"internalType":"uint64","name":"orderTime","type":"uint64"},{"indexed":false,"internalType":"uint256","name":"resalePrice","type":"uint256"}],"name":"SecondarySale","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"nftIndex","type":"uint256"},{"indexed":true,"internalType":"uint64","name":"getUsed","type":"uint64"},{"indexed":true,"internalType":"uint64","name":"orderTime","type":"uint64"}],"name":"TicketInvalidated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"nftIndex","type":"uint256"},{"indexed":true,"internalType":"uint64","name":"getUsed","type":"uint64"},{"indexed":true,"internalType":"uint64","name":"orderTime","type":"uint64"}],"name":"TicketScanned","type":"event"},{"inputs":[],"name":"CONFIGURATION","outputs":[{"internalType":"contract IGETProtocolConfiguration","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_configurationAddress","type":"address"}],"name":"__BaseGETNFT_init","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_configurationAddress","type":"address"}],"name":"__FoundationContract_init","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_originAddress","type":"address"}],"name":"addressToIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_basketContract","type":"address"}],"name":"approveBasket","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_originAddress","type":"address"},{"internalType":"uint256","name":"_orderTime","type":"uint256"}],"name":"checkIn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_originAddress","type":"address"},{"internalType":"address","name":"_externalAddress","type":"address"},{"internalType":"uint256","name":"_orderTime","type":"uint256"}],"name":"claimgetNFT","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_basketAddress","type":"address"},{"internalType":"address","name":"_eventAddress","type":"address"},{"internalType":"uint256","name":"_primaryPrice","type":"uint256"},{"internalType":"bytes32[]","name":"_ticketMetadata","type":"bytes32[]"}],"name":"collateralMint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_originAddress","type":"address"},{"internalType":"uint256","name":"_orderTime","type":"uint256"}],"name":"invalidateAddressNFT","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_nftIndex","type":"uint256"},{"internalType":"address","name":"_originAddress","type":"address"}],"name":"isNFTClaimable","outputs":[{"internalType":"bool","name":"_claim","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_nftIndex","type":"uint256"},{"internalType":"address","name":"_originAddress","type":"address"}],"name":"isNFTSellable","outputs":[{"internalType":"bool","name":"_sell","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"onChainEconomics","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_destinationAddress","type":"address"},{"internalType":"address","name":"_eventAddress","type":"address"},{"internalType":"uint256","name":"_primaryPrice","type":"uint256"},{"internalType":"uint256","name":"_basePrice","type":"uint256"},{"internalType":"uint256","name":"_orderTime","type":"uint256"},{"internalType":"bytes32[]","name":"_ticketMetadata","type":"bytes32[]"}],"name":"primarySale","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_nftIndex","type":"uint256"}],"name":"returnStructTicket","outputs":[{"components":[{"internalType":"address","name":"eventAddress","type":"address"},{"internalType":"bytes32[]","name":"ticketMetadata","type":"bytes32[]"},{"internalType":"uint32[2]","name":"salePrices","type":"uint32[2]"},{"internalType":"enum BaseGET.TicketStates","name":"state","type":"uint8"}],"internalType":"struct BaseGET.TicketData","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_originAddress","type":"address"},{"internalType":"uint256","name":"_orderTime","type":"uint256"}],"name":"scanNFT","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_originAddress","type":"address"},{"internalType":"address","name":"_destinationAddress","type":"address"},{"internalType":"uint256","name":"_orderTime","type":"uint256"},{"internalType":"uint256","name":"_secondaryPrice","type":"uint256"}],"name":"secondaryTransfer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_switchState","type":"bool"},{"internalType":"uint256","name":"_refactorSwapIndex","type":"uint256"}],"name":"setOnChainSwitch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syncConfiguration","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_originAddress","type":"address"}],"name":"ticketMetadataAddress","outputs":[{"internalType":"address","name":"_eventAddress","type":"address"},{"internalType":"bytes32[]","name":"_ticketMetadata","type":"bytes32[]"},{"internalType":"uint32[2]","name":"_salePrices","type":"uint32[2]"},{"internalType":"enum BaseGET.TicketStates","name":"_state","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_nftIndex","type":"uint256"}],"name":"ticketMetadataIndex","outputs":[{"internalType":"address","name":"_eventAddress","type":"address"},{"internalType":"bytes32[]","name":"_ticketMetadata","type":"bytes32[]"},{"internalType":"uint32[2]","name":"_salePrices","type":"uint32[2]"},{"internalType":"enum BaseGET.TicketStates","name":"_stateTicket","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_nftIndex","type":"uint256"}],"name":"viewEventOfIndex","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_nftIndex","type":"uint256"}],"name":"viewLatestResalePrice","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_nftIndex","type":"uint256"}],"name":"viewPrimaryPrice","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_nftIndex","type":"uint256"}],"name":"viewTicketMetadata","outputs":[{"internalType":"bytes32[]","name":"","type":"bytes32[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_nftIndex","type":"uint256"}],"name":"viewTicketState","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

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

# Initialize Infura
infura = Infura(w3url, nftcontract, nftabi)


def startrun():
    while True:
        fromblock = db.get_lastblock() + 1
        events, complete = infura.get_nftevents(fromBlock=fromblock)

        for event in events:
            nfttransaction = infura.get_nfttransaction(event.transactionHash)
            if nfttransaction['intputobj'].fn_name == 'primarySale':
                logprocessor.primarysalemint(event, nfttransaction, infura, db)
            elif nfttransaction['intputobj'].fn_name == 'secondaryTransfer':
                logprocessor.secondarysale(event, nfttransaction, infura, db)
            elif nfttransaction['intputobj'].fn_name == 'invalidateAddressNFT':
                logprocessor.ticketinvalidated(
                    event, nfttransaction, infura, db)
            elif nfttransaction['intputobj'].fn_name == 'scanNFT':
                logprocessor.ticketscanned(event, nfttransaction, infura, db)
            else:
                logger.warning(
                    'New kind of unproccessed log type found: {}'.format(
                    nfttransaction['intputobj'].fn_name))

        if complete == True:
            logger.info('All events are imported')
            return
        else:
            logger.info('Not all events are imported, starting new run')


while True:
    logger.info('Start run')
    startrun()
    logger.info('End run')
    time.sleep(300)
