import logging
import sqlite3
from sqlite3 import Error

# Configure logging
logger = logging.getLogger(__name__)


class Database():
    def __init__(self, db_file):
        logger.info('Start new database manager')
        self.db_file = db_file
        self.conn = None
        self.create_connection()

    def create_connection(self):
        '''create a database connection to a SQLite database'''
        logger.info('Connecting to Database')
        try:
            self.conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
        finally:
            if self.conn:
                logger.info('Database Connection Succesfull')
            else:
                logger.error("Can't connect tot he database")

    def get_upcomingevents(self, mintime, maxtime):
        '''Getting all events and tickets sold in the upcoming 7 days'''
        logger.info('Get upcoming events')
        sqlstatement = '''WITH
        inscopeevents AS(
            SELECT eventaddress,starttime,ticketeer
            FROM events
            WHERE starttime > ?
            AND starttime < ?
            AND ticketeer != "Demo"
        )
        SELECT eventname, psale.eventaddress, starttime, count(nftindex) as nfts
        FROM psale
        INNER JOIN events
        ON psale.eventaddress = events.eventaddress
        WHERE psale.eventaddress IN (SELECT eventaddress from inscopeevents)
        GROUP BY psale.eventaddress
        ORDER BY nfts DESC'''
        parameters = (mintime,maxtime)
        c = self.conn.cursor()
        try:
            c.execute(sqlstatement,parameters)
        except Exception as e:
            if e.args[0] == 'no events in specified range':
                logger.error(
                    'There are no events in the specified range')
                return []
            else:
                raise Exception('Unknown upcoming event retrieval error', e)
        f = c.fetchall()
        data = sql_to_dic(c.description, f)
        return data


    def get_tgchannels(self):
        '''Getting all tg channels registered for communication'''
        logger.debug('Get tg channels')
        sqlstatement = '''SELECT tgid,description from tgids'''
        c = self.conn.cursor()
        try:
            c.execute(sqlstatement)
        except Exception as e:
            if e.args[0] == 'no such table: tgids':
                logger.error(
                    'tgids table doesn''t exist(is the tg importer running?')
                return []
            else:
                raise Exception('Unknown TG Channels retrieval error', e)
        f = c.fetchall()
        data = sql_to_dic(c.description, f)
        return data


def sql_to_dic(description, sql):
    results = []
    for s in sql:
        dict = {}
        for i in range(0, len(description)):
            d = description[i][0]
            v = s[i]
            dict[d] = v
        results.append(dict)

    return results
