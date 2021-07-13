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
    sd = datetime(d.year,d.month,d.day)
    sdt = sd.timestamp()
    return sdt


def neweventregistered(log, eventdata, db, tg):
    logger.info('New registered event found in blocknumber: {}'.format(
        int(log['blockNumber'], 16)))

    if eventdata[9] == True:
        privateevent = 1
    else:
        privateevent = 0

    eventinfo = {
        'eventaddress': wallettostring(log['topics'][1]),
        'blocknumber': int(log['blockNumber'], 16),
        'timestamp': int(log['timeStamp'], 16),
        'timestampday': get_timestampday(int(log['timeStamp'], 16)),
        'getused': int(log['topics'][2], 16),
        'ordertime': int(log['topics'][3], 16),
        'integratoraddress': eventdata[0],
        'underwriteraddress': eventdata[1],
        'eventname': eventdata[2],
        'shopurl': eventdata[3],
        'imageurl': eventdata[4],
        'longitude': eventdata[5][0].rstrip(b'\x00').decode("utf-8"),
        'latitude': eventdata[5][1].rstrip(b'\x00').decode("utf-8"),
        'currency': eventdata[5][2].rstrip(b'\x00').decode("utf-8"),
        'ticketeer': eventdata[5][3].rstrip(b'\x00').decode("utf-8"),
        'starttime': eventdata[6][0],
        'endtime': eventdata[6][1],
        'privateevent': privateevent,
    }

    if eventinfo["ticketeer"].lower() == "demo":
        logger.info(
            'Event {} won''t be communicated because it''s a demo'.format(
                eventinfo["eventname"]))
        communicateevent = False
    else:
        communicateevent = True

    # Update event if it exists, otherwise create it
    if db.event_exists(wallettostring(log['topics'][1])):
        if communicateevent == True:
            communicate_updateevent(
                tg=tg,
                transactionhash=log['transactionHash'],
                eventname=eventinfo['eventname'],
                shopurl=eventinfo['shopurl'],
                ticketeer=eventinfo['ticketeer'],
                imageurl=eventinfo['imageurl'],
                date=eventinfo['starttime']
            )
        db.update_event(**eventinfo)
    else:
        if communicateevent == True:
            communicate_newevent(
                tg=tg,
                transactionhash=log['transactionHash'],
                eventname=eventinfo['eventname'],
                shopurl=eventinfo['shopurl'],
                ticketeer=eventinfo['ticketeer'],
                imageurl=eventinfo['imageurl'],
                date=eventinfo['starttime']
            )
        db.create_event(**eventinfo)
    return eventinfo


def communicate_newevent(
        tg, transactionhash, eventname, shopurl, ticketeer, imageurl, date):
    msg = (
        "New event registered: <b>{eventname}</b>\n"
        "TX Polygon Chain: "
        "<a href=\"https://polygonscan.com/tx/{transactionhash}\">"
        "link</a>\n"
        "Website: {shopurl}\n"
        "Date: {date}\n"
        "Ticketeer: {ticketeer}").format(
        eventname=eventname,
        transactionhash=transactionhash,
        shopurl=shopurl,
        date=datetime.fromtimestamp(date).strftime(
            '%Y-%m-%d %H:%M'),
        ticketeer=ticketeer
    )
    if '.' in imageurl:
        try:
            tg.sendphotoall(imageurl, msg)
        except Exception as e:
            if e.args[0] == 400:
                tg.sendmessageall(msg)
            else:
                raise Exception(e)
    else:
        tg.sendmessageall(msg)


def communicate_updateevent(
        tg, transactionhash, eventname, shopurl, ticketeer, imageurl, date):
    msg = (
        "Event updated: <b>{eventname}</b>\n"
        "TX Polygon Chain: "
        "<a href=\"https://polygonscan.com/tx/{transactionhash}\">"
        "link</a>\n"
        "Website: {shopurl}\n"
        "Date: {date}\n"
        "Ticketeer: {ticketeer}").format(
        eventname=eventname,
        transactionhash=transactionhash,
        shopurl=shopurl,
        date=datetime.fromtimestamp(date).strftime(
            '%Y-%m-%d %H:%M'),
        ticketeer=ticketeer
    )
    if '.' in imageurl:
        try:
            tg.sendphotoall(imageurl, msg)
        except Exception as e:
            if e.args[0] == 400:
                tg.sendmessageall(msg)
            else:
                raise Exception(e)
    else:
        tg.sendmessageall(msg)
