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

    def get_psalesummery(self, starttime, endtime):
        '''Getting the primary sales summery from the database'''
        logger.info('Gather primary sale summery')
        sqlstatement = '''SELECT eventname, count(nftindex) as nfts
            FROM psale
            INNER JOIN events
            ON events.eventaddress = psale.eventaddress
            WHERE psale.timestamp > ? AND psale.timestamp < ?
            GROUP BY eventname
            ORDER BY nfts DESC
            '''
        parameters = (starttime, endtime)
        c = self.conn.cursor()
        c.execute(sqlstatement, parameters)
        events = c.fetchall()
        return events

    def get_ssalesummery(self, starttime, endtime):
        '''Getting the secondary sales summery from the database'''
        logger.info('Gather secondary sale summery')
        sqlstatement = '''SELECT eventname, count(nftindex) as nfts
            FROM ssale
            INNER JOIN events
            ON events.eventaddress = ssale.eventaddress
            WHERE ssale.timestamp > ? AND ssale.timestamp < ?
            GROUP BY eventname
            ORDER BY nfts DESC
            '''
        parameters = (starttime, endtime)
        c = self.conn.cursor()
        c.execute(sqlstatement, parameters)
        events = c.fetchall()
        return events

    def get_tscannedsummery(self, starttime, endtime):
        '''Getting the scanned tickets summery from the database'''
        logger.info('Gather tickets scanned summery')
        sqlstatement = '''SELECT eventname, count(tscanned.nftindex) as nfts
                FROM tscanned
                INNER JOIN psale
                ON tscanned.nftindex = psale.nftindex
                INNER JOIN events
                ON psale.eventaddress = events.eventaddress
                WHERE tscanned.timestamp > ? AND tscanned.timestamp < ?
                GROUP BY eventname
                ORDER BY nfts DESC
            '''
        parameters = (starttime, endtime)
        c = self.conn.cursor()
        c.execute(sqlstatement, parameters)
        events = c.fetchall()
        return events

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
