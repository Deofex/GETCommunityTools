import logging
import psycopg2

# Configure logging
logger = logging.getLogger(__name__)


class Database():
    def __init__(
            self, dbpassword, dbuser='nftdbuser', dbname='nftdb', host='db'):
        logger.info('Start new database manager')
        self.conn = None
        self.create_connection(
            host=host, dbname=dbname, dbuser=dbuser, dbpassword=dbpassword)
        self.initialize_tables()

    def create_connection(self, host, dbname, dbuser, dbpassword):
        '''create a database connection to a SQLite database'''
        logger.info('Connecting to Database')
        try:
            self.conn = psycopg2.connect(
                host=host, dbname=dbname, user=dbuser, password=dbpassword)
        except Exception as e:
            print(e)
        finally:
            if self.conn:
                logger.info('Database Connection Succesfull')
            else:
                logger.error("Can't connect tot he database")

    def e_sqlstatement(self, sqlstatement, parameters=None):
        '''Execute SQL statement'''
        try:
            c = self.conn.cursor()
            logger.info(
                'Running SQL statement (set logging on debug for more info)')
            if parameters:
                logger.debug("Execute SQL Statement: {}. Parameters {}".format(
                    sqlstatement, parameters))
                c.execute(sqlstatement, parameters)
            else:
                logger.debug("Execute SQL Statement: {}".format(sqlstatement))
                c.execute(sqlstatement)
            self.conn.commit()
        except Exception as e:
            logger.error(e)

    def initialize_tables(self):
        '''Create the needed tables in the database'''
        logger.info("Create tables if they doesn't exist yet")
        sql_c_events_table = """ CREATE TABLE IF NOT EXISTS events (
                                    eventaddress TEXT NOT NULL,
                                    blocknumber INTEGER NOT NULL,
                                    timestamp INTEGER NOT NULL,
                                    timestampday INTEGER NOT NULL,
                                    getused INTEGER NOT NULL,
                                    ordertime INTEGER NOT NULL,
                                    integratoraddress TEXT NOT NULL,
                                    underwriteraddress TEXT NOT NULL,
                                    eventname TEXT NOT NULL,
                                    shopurl TEXT NOT NULL,
                                    imageurl TEXT NOT NULL,
                                    longitude TEXT NOT NULL,
                                    latitude TEXT NOT NULL,
                                    currency TEXT NOT NULL,
                                    ticketeer TEXT NOT NULL,
                                    starttime BIGINT NOT NULL,
                                    endtime BIGINT NOT NULL,
                                    privateevent INTEGER NOT NULL,
                                    PRIMARY KEY (eventaddress)
                                ); """

        self.e_sqlstatement(sql_c_events_table)

    def create_event(self, eventaddress, blocknumber, timestamp, timestampday,
                     getused, ordertime, integratoraddress, underwriteraddress,
                     eventname, shopurl, imageurl, longitude, latitude,
                     currency, ticketeer, starttime, endtime, privateevent):
        '''Add an event to the database'''
        logger.info("Adding an event to the database")

        parameters = (eventaddress, blocknumber, timestamp, timestampday,
                      getused, ordertime, integratoraddress, underwriteraddress,
                      eventname, shopurl, imageurl, longitude, latitude,
                      currency, ticketeer, starttime, endtime, privateevent)
        sqlstatement = ''' INSERT INTO events(
                     eventaddress, blocknumber, timestamp, timestampday,
                     getused, ordertime, integratoraddress, underwriteraddress,
                     eventname, shopurl,imageurl, longitude, latitude,
                     currency, ticketeer, starttime, endtime, privateevent
                     )
            VALUES((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),
            (%s),(%s),(%s),(%s),(%s),(%s)) '''

        self.e_sqlstatement(sqlstatement, parameters)

    def update_event(self, eventaddress, blocknumber, timestamp, timestampday,
                     getused, ordertime, integratoraddress, underwriteraddress,
                     eventname, shopurl, imageurl, longitude, latitude,
                     currency, ticketeer, starttime, endtime, privateevent):
        '''Update an event to the database'''
        logger.info("Updating an event to the database")

        parameters = (blocknumber, timestamp, timestampday, getused,
                      ordertime, integratoraddress, underwriteraddress,
                      eventname, shopurl, imageurl, longitude, latitude,
                      currency, ticketeer, starttime, endtime, privateevent,
                      eventaddress)
        sqlstatement = ''' UPDATE events
                     SET blocknumber = (%s),
                     timestamp = (%s),
                     timestampday = (%s),
                     getused = (%s),
                     ordertime = (%s),
                     integratoraddress = (%s),
                     underwriteraddress = (%s),
                     eventname = (%s),
                     shopurl = (%s),
                     imageurl = (%s),
                     longitude = (%s),
                     latitude = (%s),
                     currency = (%s),
                     ticketeer = (%s),
                     starttime = (%s),
                     endtime = (%s),
                     privateevent = (%s)
                     WHERE eventaddress = (%s)
                    '''

        self.e_sqlstatement(sqlstatement, parameters)

    def event_exists(self, eventaddress):
        '''Checks or an event exist in the database'''
        parameters = (eventaddress,)
        sqlstatement = ''' SELECT eventaddress from events
                    WHERE eventaddress = (%s) '''
        c = self.conn.cursor()
        c.execute(sqlstatement, parameters)
        returnvalue = c.fetchall()
        if len(returnvalue) == 0:
            eventexists = False
        else:
            eventexists = True
        return eventexists

    def get_lastblock(self):
        '''Getting the last block available in the database'''
        logger.info('Get last blocknumber')
        sqlstatement = '''SELECT max(blocknumber) FROM events'''
        c = self.conn.cursor()
        c.execute(sqlstatement)
        block = c.fetchall()[0][0]
        if not block:
            block = 0
        return block

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
