import sys
import os
import logging
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


def createrapport(reportdate, psalesummery, ssalesummery, tscanned):
    report = "<b>NFT report: {}-{}-{}</b>\n\n".format(
        reportdate.day, reportdate.month, reportdate.year)
    if len(psalesummery) > 0:
        i = 0
        t = 0
        report += "<b>Tickets sold on the primary market:</b>\n"
        for e in psalesummery:
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
        i = 0
        t = 0
        report += "<b>Tickets sold on the secondary market:</b>\n"
        for e in ssalesummery:
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
        i = 0
        t = 0
        report += "<b>Tickets scanned:</b>\n"
        for e in tscanned:
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
