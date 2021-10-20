import logging
from datetime import datetime

# Initialize logger
logger = logging.getLogger(__name__)

def get_timestampday(timestamp):
    d = datetime.fromtimestamp(timestamp)
    sd = datetime(d.year, d.month, d.day)
    sdt = sd.timestamp()
    return sdt


def primarysalemint(event, nfttransaction,infura, db):
    logger.info('New primary sale mint found in blocknumber: {}'.format(
        nfttransaction['transaction'].blockNumber))

    eventdata = infura.get_eventresults(event,"PrimarySaleMint")

    ticketinfo = {
        'nftindex': eventdata.args.nftIndex,
        'blocknumber': eventdata.blockNumber,
        'timestamp': eventdata.args.orderTime,
        'timestampday': get_timestampday(eventdata.args.orderTime),
        'getused': int(eventdata.args.getUsed),
        'ordertime': int(eventdata.args.orderTime),
        'destinationaddress': nfttransaction['intputpar']['_destinationAddress'],
        'eventaddress': nfttransaction['intputpar']['_eventAddress'],
        'price': nfttransaction['intputpar']['_basePrice']
    }

    db.create_psale(**ticketinfo)
    return ticketinfo
