import logging
import requests
import time
from web3 import Web3

# Initialize logger
logger = logging.getLogger(__name__)


def get_url(url, headers=None):
    '''Retrieve content from an URL'''
    logger.debug('Getting content from: {}'.format(url))
    response = requests.get(url, headers=headers)
    content = response.content.decode("utf8")
    return content


def connect_w3(w3url):
    '''Connect to the bscprovider'''
    logger.info('Connect with w3 provider via URL: {}'.format(w3url))
    w3_provider = Web3.HTTPProvider(w3url)
    w3 = Web3(w3_provider)
    return w3


def load_w3contract(w3, contractaddress, abiurl):
    '''Load the w3 contract'''
    # Load the GET ABI from a file
    logger.info('Load w3 contract from address'.format(contractaddress))
    abi = get_url(abiurl)
    contractaddress = Web3.toChecksumAddress(contractaddress)
    contract = w3.eth.contract(address=contractaddress, abi=abi)
    return contract

def wallettostring(wallet):
    ws = "{0:#0{1}x}".format(int(wallet, 16), 1)
    if len(ws) < 42:
        addzeros = 42 - len(ws)
        ws = ws.replace("0x", "0x" + "0" * addzeros)
    return ws

def get_w3eventdata(eventscontract,eventaddress):
    logger.info('Get w3 event data for event: {}'.format('eventaddress'))
    eventaddresschecksum = Web3.toChecksumAddress(
        wallettostring(eventaddress))
    retry = 0
    while True:
        try:
            e = eventscontract.functions.getEventData(
                eventaddresschecksum).call()
            return e
        except Exception as e:
            if e.args[0]['code'] == -32603:
                if retry < 5:
                    logger.warning('A timeout has occured, retry in 10 seconds')
                    time.sleep(10)
                    retry += 1
                else:
                    logger.error('5 timeouts in a row, cannot continue')
            else:
                logger.error(
                    'Error occured getting w3 events. Error: {}: {}'.format(
                        e.args[0]['code'], e.args[0]['message']
                    ))
                raise Exception('Unknown error occured')
