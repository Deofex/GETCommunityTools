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
    def __init__(self,telegramapitoken):
        self.apikey = telegramapitoken
        self.offset = 0

    def getmessages(self):
        method = "getUpdates"
        offset = str(self.offset + 1)
        parameters = {
            "timeout": 300,
            "offset": offset
        }
        getmessageurl = self.createtelegramurl(method, parameters=parameters)
        logger.debug("Get new updates via url: {}".format(getmessageurl))
        results = get_json_from_url(getmessageurl)
        if len(results['result']) > 0:
            self.offset = int(results['result'][-1]['update_id'])

        return results

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
