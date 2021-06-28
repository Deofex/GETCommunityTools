import logging

# Initialize logger
logger = logging.getLogger(__name__)


def wallettostring(wallet):
    ws = "{0:#0{1}x}".format(int(wallet, 16), 1)
    if len(ws) < 42:
        addzeros = 42 - len(ws)
        ws = ws.replace("0x", "0x" + "0" * addzeros)
    return ws


def ticketinvalidated(log,db):
    logger.info('New ticket invalidated found in blocknumber: {}'.format(
        int(log['blockNumber'], 16)))

    invalidateinfo = {
        'nftindex':int(log['topics'][1], 16),
        'blocknumber':int(log['blockNumber'], 16),
        'timestamp':int(log['timeStamp'], 16),
        'getused':int(log['topics'][2], 16),
        'ordertime':int(log['topics'][3], 16),
        'originaddress':wallettostring(log['data']),
        }

    db.create_tinvalidated(**invalidateinfo)
    return invalidateinfo
