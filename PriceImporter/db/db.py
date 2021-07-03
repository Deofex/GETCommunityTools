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
        sql_c_prices_table = """ CREATE TABLE IF NOT EXISTS prices (
                                    token TEXT NOT NULL,
                                    price FLOAT NOT NULL,
                                    PRIMARY KEY (token)
                                ); """
        self.e_sqlstatement(sql_c_prices_table)

    def create_price(self, token, price):
        '''Add a primary sale to the database'''
        logger.info("Adding a price to the database")

        parameters = (token, price)
        sqlstatement = ''' INSERT INTO prices(
            token, price)
            VALUES((%s),(%s)) '''

        self.e_sqlstatement(sqlstatement, parameters)

    def update_price(self, token, price):
        '''Update a price in the database'''
        logger.info("Updating a price in the database")

        parameters = (price, token)
        sqlstatement = ''' UPDATE prices
                     SET price = (%s)
                     WHERE token = (%s)
                    '''

        self.e_sqlstatement(sqlstatement, parameters)

    def get_price(self, token):
        '''Getting token price'''
        logger.debug('Get token price')
        parameters = (token,)
        sqlstatement = '''SELECT price FROM prices WHERE token = (%s)'''
        c = self.conn.cursor()
        c.execute(sqlstatement,parameters)
        f = c.fetchall()
        if len(f) == 0:
            price = None
        else:
            price = f[0][0]
        return price


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
