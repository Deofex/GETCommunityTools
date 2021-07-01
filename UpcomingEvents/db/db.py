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

    def get_upcomingevents(self, mintime, maxtime):
        '''Getting all events and tickets sold in the upcoming 7 days'''
        logger.info('Get upcoming events')
        sqlstatement = '''WITH
        inscopeevents AS(
            SELECT eventaddress,starttime,eventname
            FROM events
            WHERE starttime BETWEEN (%s) AND (%s)
            AND ticketeer != 'Demo'
        )
        SELECT eventname, psale.eventaddress, starttime, count(nftindex) as nfts
        FROM psale
        INNER JOIN inscopeevents
        ON psale.eventaddress = inscopeevents.eventaddress
        WHERE psale.eventaddress IN (SELECT eventaddress from inscopeevents)
        GROUP BY psale.eventaddress, eventname, starttime
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
