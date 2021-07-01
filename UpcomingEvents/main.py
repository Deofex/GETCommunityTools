import sys
import os
import logging
from datetime import datetime
from db.db import Database
from telegram.telegram import TelegramBot

# Log level 1 is INFO, Log level 2 is Debug
loglevel = int(os.environ.get('loglevel'))
# Database password
dbpassword = os.environ.get('POSTGRES_PASSWORD')
# Telegram API Token
telegramapitoken = os.environ.get('telegramapitoken')

# Configure the logger
if loglevel == 1:
    loglevel = logging.INFO
elif loglevel == 2:
    loglevel = logging.DEBUG
logging.basicConfig(
    format=('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
    datefmt="%a %d/%m/%Y %H:%M:%S",
    level=loglevel,
    stream=sys.stdout)

# Initialize logger
logger = logging.getLogger(__name__)
logger.info('Start Reporter processor')

# Initialize Database
db = Database(dbpassword)

# Initialize bot
tg = TelegramBot(telegramapitoken, db)


def combine_events(events):
    cevents = {}
    for e in events:
        if e['eventname'] in cevents:
            cevents[e['eventname']][0] = True
            cevents[e['eventname']][1].append(datetime.fromtimestamp(
                e['starttime']).strftime('%Y-%m-%d %H:%M'))
            cevents[e['eventname']][2] += e['nfts']
        else:
            eventdata = [
                False,
                [datetime.fromtimestamp(e['starttime']).strftime(
                    '%Y-%m-%d %H:%M'), ],
                e['nfts']
            ]
            cevents[e['eventname']] = eventdata

    ceventsdict = []
    for key, value in cevents.items():
        ceventsdict.append({
            'eventname': key,
            'multievent': value[0],
            'date': value[1],
            'ticketssold': value[2]
        })

    ceventsdict = sorted(
        ceventsdict, key=lambda i: i['ticketssold'], reverse=True)

    return ceventsdict


def create_report(combinedevents, days):
    msg = ('<b>Upcoming event report</b>\nIn the upcoming {} days, the '
           'following events will take place.\n\n'.format(days))

    for e in combinedevents:
        if e['multievent'] == True:
            msg += ('<b>{eventname}</b>\n   Date: {occurrences} occurrences\n'
                    '   Tickets sold:{ticketssold}\n'.format(
                        eventname=e['eventname'],
                        occurrences=len(e['date']),
                        ticketssold=e['ticketssold']
                    ))
        else:
            msg += ('<b>{eventname}</b>\n   Date: {date}\n   '
                    'Tickets sold: {ticketssold}\n'.format(
                        eventname=e['eventname'],
                        date=e['date'][0],
                        ticketssold=e['ticketssold']
                    ))
    return msg


def getdayreport():
    days = 7
    # Set current timestamp + calculate the timestamp in 1 week
    ct = datetime.now().timestamp()
    wt = ct + (60*60*24*days)
    # Get the events starting in this range
    events = db.get_upcomingevents(ct, wt)
    combinedevents = combine_events(events)
    msg = create_report(combinedevents, days)
    return msg


msg = getdayreport()
tg.sendmessageall(msg)
