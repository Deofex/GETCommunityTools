import logging

# Initialize logger
logger = logging.getLogger(__name__)


def wallettostring(wallet):
    ws = "{0:#0{1}x}".format(int(wallet, 16), 1)
    if len(ws) < 42:
        addzeros = 42 - len(ws)
        ws = ws.replace("0x", "0x" + "0" * addzeros)
    return ws


def nftminted(log,db):
    # This function gives an error, because it's phased out from the database
    # will be removed completely later on
    logger.info('New nft mint found in blocknumber: {}'.format(
        int(log['blockNumber'], 16)))

    mintinfo = {
        'nftindex':int(log['topics'][1], 16),
        'blocknumber':int(log['blockNumber'], 16),
        'timestamp':int(log['timeStamp'], 16),
        'destinationaddress':wallettostring(log['topics'][2])
        }

    db.create_nftmint(**mintinfo)
    return mintinfo