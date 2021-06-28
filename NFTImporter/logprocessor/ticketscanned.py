import logging

# Initialize logger
logger = logging.getLogger(__name__)


def ticketscanned(log,db):
    logger.info('New ticket scanned found in blocknumber: {}'.format(
        int(log['blockNumber'], 16)))

    scaninfo = {
        'nftindex':int(log['topics'][1], 16),
        'blocknumber':int(log['blockNumber'], 16),
        'timestamp':int(log['timeStamp'], 16),
        'getused':int(log['topics'][2], 16),
        'ordertime':int(log['topics'][3], 16)
        }

    db.create_tscanned(**scaninfo)
    return scaninfo
