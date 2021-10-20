import logging
from web3 import Web3
from web3._utils.events import get_event_data


# Configure logging
logger = logging.getLogger(__name__)


class Infura():
    def __init__(self, w3url, nftcontract, nftabi):
        logger.info('Initialize Infura handler')
        self.w3url = w3url
        self.nftcontractaddress = nftcontract
        self.nftabi = nftabi

        # Connect to Web3 via the web3 url provided
        self.w3 = Web3(Web3.HTTPProvider(
            w3url,
            request_kwargs={'timeout': 100}))

        # Load NFT contract
        self.nftcontract = self.w3.eth.contract(
            address=nftcontract, abi=nftabi)

    def get_nftevents(self, fromBlock, toBlock='latest'):
        logger.info('Retrieving NFT events. Fromblock: {} - ToBlock: {}'.format(
            fromBlock, toBlock
        ))
        events = self.w3.eth.get_logs({
            'fromBlock': fromBlock,
            'toBlock': toBlock,
            'address': self.nftcontractaddress
        })
        return events

    def get_nfttransaction(self, txhash):
        logger.info('Get Infura transaction with tx hash: {}'.format(
            txhash.hex()))
        t = self.w3.eth.get_transaction(txhash)
        intputobj, intputpar = self.nftcontract.decode_function_input(t.input)
        nfttransaction = {
            'transaction': t,
            'intputobj': intputobj,
            'intputpar': intputpar
        }
        return nfttransaction

    def get_eventresults(self, event, templatename):
        template = eval("self.nftcontract.events." + templatename)
        results = get_event_data(
            template.web3.codec, template._get_event_abi(), event)
        return results