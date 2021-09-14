import logging
from datetime import datetime

# Initialize logger
logger = logging.getLogger(__name__)


def wallettostring(wallet):
    ws = "{0:#0{1}x}".format(int(wallet, 16), 1)
    if len(ws) < 42:
        addzeros = 42 - len(ws)
        ws = ws.replace("0x", "0x" + "0" * addzeros)
    return ws


def get_timestampday(timestamp):
    d = datetime.fromtimestamp(timestamp)
    sd = datetime(d.year, d.month, d.day)
    sdt = sd.timestamp()
    return sdt


def primarysalemint(log, db):
    logger.info('New primary sale mint found in blocknumber: {}'.format(
        int(log['blockNumber'], 16)))

    ticketinfo = {
        'nftindex': int(log['topics'][1], 16),
        'blocknumber': int(log['blockNumber'], 16),
        'timestamp': int(log['timeStamp'], 16),
        'timestampday': get_timestampday(int(log['timeStamp'], 16)),
        'getused': int(log['topics'][2], 16),
        'ordertime': int(log['topics'][3], 16),
        'destinationaddress': wallettostring(log['data'][:66]),
        'eventaddress': wallettostring("0x" + log['data'][67:130]),
        'price': int("0x" + log['data'][135:200], 16)
    }

    db.create_psale(**ticketinfo)
    return ticketinfo
