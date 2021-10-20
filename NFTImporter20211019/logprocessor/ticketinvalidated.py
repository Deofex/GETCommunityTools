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


def ticketinvalidated(event, nfttransaction, infura, db):
    logger.info('New ticket invalidated found in blocknumber: {}'.format(
        nfttransaction['transaction'].blockNumber))

    eventdata = infura.get_eventresults(event,"TicketInvalidated")

    invalidateinfo = {
        'nftindex': eventdata.args.nftIndex,
        'blocknumber': eventdata.blockNumber,
        'timestamp': eventdata.args.orderTime,
        'timestampday': get_timestampday(eventdata.args.orderTime),
        'getused': eventdata.args.getUsed,
        'ordertime': eventdata.args.orderTime,
        'originaddress': nfttransaction['intputpar']['_originAddress']
    }

    db.create_tinvalidated(**invalidateinfo)
    return invalidateinfo
