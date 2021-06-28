import time
import logging
import json
import requests

# Configure logging
logger = logging.getLogger(__name__)


def get_url(url, headers=None):
    '''Retrieve content from an URL'''
    response = requests.get(url, headers=headers)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url, headers=None):
    '''Retrieve a JSON file from an URL'''
    content = get_url(url, headers)
    js = json.loads(content)
    return js


class TelegramBot():
    def __init__(self, telegramapitoken, db):
        self.apikey = telegramapitoken
        self.offset = 0
        self.db = db

    def createtelegramurl(self, method, parameters={}):
        # Define api url
        turl = "https://api.telegram.org/bot{}/{}".format(
            self.apikey, method)

        # Add parameters to the api url
        if len(parameters.keys()) != 0:
            turl = turl + "?"
            for parameter in parameters.keys():
                turl = turl + parameter + "="
                turl = turl + str(parameters[parameter]) + "&"

        # Remove last &
        turl = turl[:-1]

        logger.debug("Telegram API url: {}".format(turl))
        return turl

    def removemessage(self, chat_id, message_id):
        method = 'deleteMessage'
        parameters = {
            'chat_id': chat_id,
            'message_id': message_id
        }
        getmessageurl = self.createtelegramurl(method, parameters=parameters)
        logger.debug("Remove message via url: {}".format(getmessageurl))
        results = get_json_from_url(getmessageurl)
        if results['ok']:
            logger.debug("Message removed succesfully")
        else:
            logger.warning("Can't remove /Start message")
        return results

    def sendmessage(
            self, chatid, msg, formatstyle="HTML", disablewebpreview="True"):
        method = 'sendMessage'
        parameters = {
            "chat_id": chatid,
            "text": msg,
            "parse_mode": formatstyle,
            "disable_web_page_preview": disablewebpreview
        }
        getmessageurl = self.createtelegramurl(method, parameters=parameters)
        logger.debug("Send message via url: {}".format(getmessageurl))
        results = get_json_from_url(getmessageurl)
        return results

    def sendmessageall(self, msg):
        tgids = self.db.get_tgchannels()
        for tgid in tgids:
            chatid = tgid['tgid']
            logger.debug("Send msg: {} to chatid: {}".format(msg, chatid))
            while True:
                msgresult = self.sendmessage(chatid, msg)
                if msgresult['ok'] == False:
                    if msgresult['error_code'] == 429:
                        logger.info('Rate request exceeded, waiting 60 sec')
                        time.sleep(60)
                    else:
                        break
                else:
                    break
            time.sleep(3)
