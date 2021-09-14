import logging
import psycopg2

# Configure logging
logger = logging.getLogger(__name__)


class Database():
    def __init__(
        self, dbpassword, dbuser='nftdbuser', dbname='nftdb',host= 'db'):
        logger.info('Start new database manager')
        self.conn = None
        self.create_connection(
            host=host,dbname=dbname, dbuser=dbuser, dbpassword=dbpassword)

    def create_connection(self, host, dbname, dbuser, dbpassword):
        '''create a database connection to a SQLite database'''
        logger.info('Connecting to Database')
        try:
            self.conn =  psycopg2.connect(
                host=host, dbname=dbname, user=dbuser, password=dbpassword)
        except Exception as e:
            print(e)
        finally:
            if self.conn:
                logger.info('Database Connection Succesfull')
            else:
                logger.error("Can't connect tot he database")

    def get_psalesummery(self, starttime, endtime):
        '''Getting the primary sales summery from the database'''
        logger.info('Gather primary sale summery')
        sqlstatement = '''SELECT eventname, count(nftindex) as nfts, ticketeer
            FROM psale
            LEFT JOIN events
            ON events.eventaddress = psale.eventaddress
            WHERE psale.timestamp BETWEEN (%s) AND (%s)
            GROUP BY eventname, ticketeer
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
        sqlstatement = '''SELECT eventname, count(nftindex) as nfts, ticketeer
            FROM ssale
            LEFT JOIN events
            ON events.eventaddress = ssale.eventaddress
            WHERE ssale.timestamp BETWEEN (%s) AND (%s)
            GROUP BY eventname, ticketeer
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
        sqlstatement = '''
                SELECT eventname, count(tscanned.nftindex) as nfts, ticketeer
                FROM tscanned
                INNER JOIN psale
                ON tscanned.nftindex = psale.nftindex
                LEFT JOIN events
                ON psale.eventaddress = events.eventaddress
                WHERE tscanned.timestamp BETWEEN (%s) AND (%s)
                GROUP BY eventname, ticketeer
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
