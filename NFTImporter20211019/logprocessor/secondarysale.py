import logging
from datetime import datetime

# Initialize logger
logger = logging.getLogger(__name__)

def get_timestampday(timestamp):
    d = datetime.fromtimestamp(timestamp)
    sd = datetime(d.year, d.month, d.day)
    sdt = sd.timestamp()
    return sdt


def secondarysale(event, nfttransaction, infura, db):
    logger.info('New secondary sale found in blocknumber: {}'.format(
        nfttransaction['transaction'].blockNumber))

    eventdata = infura.get_eventresults(event,"SecondarySale")

    ticketinfo = {
        'nftindex': eventdata.args.nftIndex,
        'blocknumber': eventdata.blockNumber,
        'timestamp': eventdata.args.orderTime,
        'timestampday': get_timestampday(eventdata.args.orderTime),
        'getused': eventdata.args.getUsed,
        'ordertime': eventdata.args.orderTime,
        'destinationaddress': nfttransaction['intputpar']['_destinationAddress'],
        'eventaddress': '0x0000000000000000000000000000000000000000',
        'price': nfttransaction['intputpar']['_secondaryPrice']
    }

    db.create_ssale(**ticketinfo)
    return ticketinfo
