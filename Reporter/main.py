import sys
import os
import logging
import re
from datetime import datetime, time, timedelta
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
tg = TelegramBot(telegramapitoken,db)


def filtersummery(summery):
    # Your ticket provider guid in regex format + counter
    ytpguidregex = '^([0-z]){8}(-([0-z]){4}){3}-([0-z]){12}$'
    filtersummery = {}

    for e in summery:
        if e[0] == None:
            n = 'Unregistered/Private events'
        if re.match(ytpguidregex, e[0]) and e[2] == 'YourTicketProvider':
            n = 'YourTicketProvider events (nameless)'
        else:
            n = e[0]
        # If event exist, update the amount, else create a new entry
        if n in filtersummery.keys():
            filtersummery[n] = filtersummery[n] + e[1]
        else:
            filtersummery[n] = e[1]

        # sort events
        sortedfilteredsum = dict(sorted(
            filtersummery.items(), key=lambda item: item[1], reverse=True))
    return sortedfilteredsum



def createrapport(reportdate, psalesummery, ssalesummery, tscanned):
    report = "<b>NFT report: {}-{}-{}</b>\n\n".format(
        reportdate.day, reportdate.month, reportdate.year)
    if len(psalesummery) > 0:
        filteredpsalesummery = filtersummery(psalesummery)
        i = 0
        t = 0
        report += "<b>Tickets sold on the primary market:</b>\n"
        for e in filteredpsalesummery.items():
            if e[0] == None:
                n = 'Unregistered/Private events'
            else:
                n = e[0]
            i += 1
            t += e[1]
            report += ("<b>{})</b> {} --> {}\n".format(
                i, n, e[1]))
        report += '<b>Total Amount: {}</b>\n\n'.format(t)
    if len(ssalesummery) > 0:
        filteredssalesummery = filtersummery(ssalesummery)
        i = 0
        t = 0
        report += "<b>Tickets sold on the secondary market:</b>\n"
        for e in filteredssalesummery.items():
            if e[0] == None:
                n = 'Unregistered/Private events'
            else:
                n = e[0]
            i += 1
            t += e[1]
            report += ("<b>{})</b> {} --> {}\n".format(
                i, n, e[1]))
        report += '<b>Total Amount: {}</b>\n\n'.format(t)
    if len(tscanned) > 0:
        filteredtscanned = filtersummery(tscanned)
        i = 0
        t = 0
        report += "<b>Tickets scanned:</b>\n"
        for e in filteredtscanned.items():
            if e[0] == None:
                n = 'Unregistered/Private events'
            else:
                n = e[0]
            i += 1
            t += e[1]
            report += ("<b>{})</b> {} --> {}\n".format(
                i, n, e[1]))
        report += '<b>Total Amount: {}</b>\n\n'.format(t)

    report += ("<a href=\"https://explorer.get-protocol.io/\">"
    "All actions above are performed on getNFTs minted on  "
    "Polygon. View all NFT's in the GET ticket explorer</a>\n")

    return report


def getdayreport():
    # Calculate starttime (st) and endtime (et) in epoch format
    ct = datetime.now()
    reportdate = datetime(ct.year, ct.month, ct.day) - timedelta(1)
    st = reportdate.timestamp()
    et = datetime(ct.year, ct.month, ct.day).timestamp()

    logger.info('Creating report for: {}'.format(reportdate))
    # Gather the primary sale summery from the database
    psalesummery = db.get_psalesummery(st, et)
    # Gather the secondary sale summery from the database
    ssalesummery = db.get_ssalesummery(st, et)
    # Gether the scanned ticket sumemry from the database
    tscanned = db.get_tscannedsummery(st, et)
    # Create the report
    report = createrapport(reportdate, psalesummery, ssalesummery, tscanned)
    logger.info('Report created: {}'.format(report))
    return report


msg = getdayreport()
tg.sendmessageall(msg)
