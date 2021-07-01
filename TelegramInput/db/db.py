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
        self.initialize_tables()

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
            print(e)

    def initialize_tables(self):
        '''Create the needed tables in the database'''
        # Beware that other containers use the same DB
        logger.info("Create tgids table if it doesn't exist yet")
        sql_c_telegramchannels_table = """ CREATE TABLE IF NOT EXISTS tgids (
                                    tgid TEXT NOT NULL,
                                    description TEXT NOT NULL,
                                    PRIMARY KEY (tgid)
                                ); """
        self.e_sqlstatement(sql_c_telegramchannels_table)

    def check_telegramidexist(self, tgid):
        '''Checks or Telegram ID exist in database'''
        logger.debug('Check or tgid {} exists'.format(tgid))
        parameters = (str(tgid),)
        sqlstatement = '''SELECT EXISTS(
                SELECT * FROM tgids WHERE tgid=((%s))
            );
        '''
        c = self.conn.cursor()
        c.execute(sqlstatement, parameters)
        r = c.fetchall()[0][0]
        if r == 1:
            logger.debug('Tgid {} exists'.format(tgid))
            return True
        else:
            logger.debug('Tgid {} doesn''t exist'.format(tgid))
            return False


    def add_telegramid(self, tgid, description):
        '''Add a tgid to the database'''
        logger.info("Adding a tgids to the database")

        parameters = (tgid, description)
        sqlstatement = ''' INSERT INTO tgids(
            tgid, description)
            VALUES((%s),(%s)) '''

        self.e_sqlstatement(sqlstatement, parameters)

