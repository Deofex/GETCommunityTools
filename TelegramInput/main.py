import sys
import os
import logging
import time
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
logger.info('Start Telegram input processor')

#Initialize Database
db = Database(dbpassword)

# Initialize bot
tgbot = TelegramBot(telegramapitoken)

while True:
    newmessages = tgbot.getmessages()
    for m in newmessages['result']:
        if 'message' in m:
            if 'text' not in m['message']:
                continue
            if m['message']['text'].lower() != '/start':
                continue
            id = m['message']['chat']['id']
            username = m['message']['chat']['username']
            logger.info("/Start from: {} - {}".format(
                id, username))
            # If the id is not in the database add it
            if not db.check_telegramidexist(id):
                logger.info("Add telegram ID {} in the database".format(id))
                db.add_telegramid(id, username)
        if 'channel_post' in m:
            if m['channel_post']['text'].lower() != '/start':
                continue
            id = m['channel_post']['chat']['id']
            username = m['channel_post']['chat']['username']
            msgid = m['channel_post']['message_id']
            tgbot.removemessage(id,msgid)
            logger.info("/Start from: {} - {} (CHANNEL!)".format(
                id, username))
            # If the id is not in the database add it
            if not db.check_telegramidexist(id):
                logger.info("Add telegram ID {} in the database".format(id))
                db.add_telegramid(id, username)
            else :
                logger.info("Telegram ID {} already in the database".format(id))
    time.sleep(1)



