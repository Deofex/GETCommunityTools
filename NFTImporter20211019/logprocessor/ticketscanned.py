import logging
from datetime import datetime

# Initialize logger
logger = logging.getLogger(__name__)


def get_timestampday(timestamp):
    d = datetime.fromtimestamp(timestamp)
    sd = datetime(d.year, d.month, d.day)
    sdt = sd.timestamp()
    return sdt


def ticketscanned(event, nfttransaction, infura, db):
    logger.info('New ticket scanned found in blocknumber: {}'.format(
        nfttransaction['transaction'].blockNumber))

    eventdata = infura.get_eventresults(event,"TicketScanned")

    scaninfo = {
        'nftindex': eventdata.args.nftIndex,
        'blocknumber': eventdata.blockNumber,
        'timestamp': eventdata.args.orderTime,
        'timestampday': get_timestampday(eventdata.args.orderTime),
        'getused': eventdata.args.getUsed,
        'ordertime': eventdata.args.orderTime
    }

    db.create_tscanned(**scaninfo)
    return scaninfo
