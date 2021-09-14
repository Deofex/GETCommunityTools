import time
import requests
import json
import logging


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


def get_json_with_check(url):
    '''Get JSON file and check or the data is valid, JSON need to have a status
    message (status 1 is okay)'''
    while True:
        try:
            logger.debug('JSON with check. URL: {}'.format(url))
            data = get_json_from_url(url)
            logger.debug('JSON reply recieved')
            # JSON Status response 1 is okay, otherwise there's an error
            if data['status'] == '1' or data['message'] == 'No records found':
                logger.debug('JSON reply is valid ')
                break
            else:
                logger.error("JSON status retrieved: {} from url: {}".format(
                    data['status'], url))
                logger.error('JSON response invalid, retry in 60 sec')
                time.sleep(60)
        except:
            logger.error(('Can''t retrieve correct JSON file from url : {}, '
                          'retry in 60 sec').format(url))
            time.sleep(60)

    return data


def get_logsapi(contract, polygonscanapikey, fromblock=0, toblock='latest'):
    '''
    Collect logs from the blockchain (unfiltered, no checks on max logs etc.)
    '''
    url = ("https://api.polygonscan.com/api?module=logs&action=getLogs"
           "&fromBlock={}"
           "&toBlock={}"
           "&address={}"
           "&apikey={}".format(fromblock, toblock,
                               contract, polygonscanapikey))
    data = get_json_with_check(url)

    return data


def get_highestblock(batch):
    fromblock = 0
    i= 0
    for r in batch:
        blockhexstr = r['blockNumber']
        blockint = int(blockhexstr, 16)
        if blockint > fromblock:
            lastblockhexstr = blockhexstr
            fromblock = blockint
            logger.debug("{}) Fromblock {}  ------ {} higher".format(i,blockhexstr,blockint))
        elif blockint == fromblock:
            logger.debug("{}) Fromblock {}  ------ {} equal".format(i,blockhexstr,blockint))
        else:
            logger.debug("{}) Fromblock {}  ------ {} lower".format(i,blockhexstr,blockint))
        i = i + 1
    return lastblockhexstr, fromblock


class BlockchainLogImporter():
    def __init__(self, polygonscanapikey, nftcontract):
        self.polygonscanapikey = polygonscanapikey
        self.nftcontract = nftcontract

    def get_logs(self,fromblock=0):
        '''Collect logs'''
        logging.info(
            "Collecting logs, starting at block: {}".format(fromblock))
        logs = []
        finished = False
        while finished != True:
            data = get_logsapi(fromblock=fromblock,
            polygonscanapikey=self.polygonscanapikey,
            contract=self.nftcontract)
            # If the amount of logs > 1000, the maximum amount is reached
            # Looping through the logs until less than 1000 are collected in 1
            # batch
            if len(data['result']) == 1000:
                logger.info(
                    'More than 1000 logs recieved, more runs required')
                # Results are unsorted, get the highest block
                lastblockhexstr, fromblock = get_highestblock(data['result'])
                # Remove lastblock, to avoid duplicated data
                filtereddata = [data for data in data['result']
                                if data['blockNumber'] != lastblockhexstr]
                logger.info("Block in batch: {} - {}".format(
                    int(data['result'][0]['blockNumber'], 16),
                    fromblock))
            else:
                filtereddata = data['result']
                finished = True

            for log in filtereddata:
                logs.append(log)
        logger.info("{} logs found.".format(len(logs)))

        return logs


# Initialize logger
logger = logging.getLogger(__name__)
