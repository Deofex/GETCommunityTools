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
        self.initialize_tables()

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
        except Error as e:
            print(e)

    def initialize_tables(self):
        '''Create the needed tables in the database'''
        logger.info("Create tables if they doesn't exist yet")
        sql_c_psale_table = """ CREATE TABLE IF NOT EXISTS psale (
                                    nftindex INTEGER NOT NULL,
                                    blocknumber INTEGER NOT NULL,
                                    timestamp INTEGER NOT NULL,
                                    getused INTEGER NOT NULL,
                                    ordertime INTEGER NOT NULL,
                                    destinationaddress TEXT NOT NULL,
                                    eventaddress TEXT NOT NULL,
                                    price INTEGER NOT NULL
                                ); """
        sql_c_ssale_table = """ CREATE TABLE IF NOT EXISTS ssale (
                                    nftindex INTEGER NOT NULL,
                                    blocknumber INTEGER NOT NULL,
                                    timestamp INTEGER NOT NULL,
                                    getused INTEGER NOT NULL,
                                    ordertime INTEGER NOT NULL,
                                    destinationaddress TEXT NOT NULL,
                                    eventaddress TEXT NOT NULL,
                                    price INTEGER NOT NULL
                                ); """
        sql_c_nftminted_table = """ CREATE TABLE IF NOT EXISTS nftminted (
                                    nftindex INTEGER NOT NULL PRIMARY KEY,
                                    blocknumber INTEGER NOT NULL,
                                    timestamp INTEGER NOT NULL,
                                    destinationaddress TEXT NOT NULL
                                ); """
        sql_c_tinvalidated_table = """ CREATE TABLE IF NOT EXISTS tinvalidated (
                                    nftindex INTEGER NOT NULL PRIMARY KEY,
                                    blocknumber INTEGER NOT NULL,
                                    timestamp INTEGER NOT NULL,
                                    getused INTEGER NOT NULL,
                                    ordertime INTEGER NOT NULL,
                                    originaddress TEXT NOT NULL
                                ); """
        sql_c_tscanned_table = """ CREATE TABLE IF NOT EXISTS tscanned (
                                    nftindex INTEGER NOT NULL PRIMARY KEY,
                                    blocknumber INTEGER NOT NULL,
                                    timestamp INTEGER NOT NULL,
                                    getused INTEGER NOT NULL,
                                    ordertime INTEGER NOT NULL
                                ); """
        self.e_sqlstatement(sql_c_psale_table)
        self.e_sqlstatement(sql_c_ssale_table)
        self.e_sqlstatement(sql_c_nftminted_table)
        self.e_sqlstatement(sql_c_tinvalidated_table)
        self.e_sqlstatement(sql_c_tscanned_table)

    def create_psale(self, nftindex, blocknumber, timestamp, getused,
                     ordertime, destinationaddress, eventaddress,
                     price):
        '''Add a primary sale to the database'''
        logger.info("Adding a primary sale to the database")

        parameters = (nftindex, blocknumber, timestamp, getused,
                      ordertime, destinationaddress, eventaddress,
                      price)
        sqlstatement = ''' INSERT INTO psale(
            nftindex, blocknumber, timestamp, getused,
            ordertime, destinationaddress, eventaddress, price)
            VALUES(?,?,?,?,?,?,?,?) '''

        self.e_sqlstatement(sqlstatement, parameters)

    def create_ssale(self, nftindex, blocknumber, timestamp, getused,
                     ordertime, destinationaddress, eventaddress,
                     price):
        '''Add a secondary sale to the database'''
        logger.info("Adding a secondary sale to the database")

        parameters = (nftindex, blocknumber, timestamp, getused,
                      ordertime, destinationaddress, eventaddress,
                      price)
        sqlstatement = ''' INSERT INTO ssale(
            nftindex, blocknumber, timestamp, getused,
            ordertime, destinationaddress, eventaddress, price)
            VALUES(?,?,?,?,?,?,?,?) '''

        self.e_sqlstatement(sqlstatement, parameters)

    def create_nftmint(self, nftindex, blocknumber, timestamp,
                       destinationaddress):
        '''Add a NFT mint to the database'''
        logger.info("Adding a NFT mint to the database")

        parameters = (nftindex, blocknumber, timestamp, destinationaddress)
        sqlstatement = ''' INSERT INTO nftminted(
            nftindex, blocknumber, timestamp, destinationaddress)
            VALUES(?,?,?,?) '''

        self.e_sqlstatement(sqlstatement, parameters)

    def create_tinvalidated(self, nftindex, blocknumber, timestamp,
                           getused, ordertime, originaddress):
        '''Add a ticket invalidation to the database'''
        logger.info("Adding a ticket invalidation to the database")

        parameters = (nftindex, blocknumber, timestamp,
                      getused, ordertime, originaddress)
        sqlstatement = ''' INSERT INTO tinvalidated(
            nftindex, blocknumber, timestamp, getused, ordertime, originaddress)
            VALUES(?,?,?,?,?,?) '''

        self.e_sqlstatement(sqlstatement, parameters)

    def create_tscanned(self, nftindex, blocknumber, timestamp,getused,
    ordertime):
        '''Add a ticket scanto the database'''
        logger.info("Adding a ticket scan to the database")

        parameters = (nftindex, blocknumber, timestamp, getused, ordertime)
        sqlstatement = ''' INSERT INTO tscanned(
            nftindex, blocknumber, timestamp, getused, ordertime)
            VALUES(?,?,?,?,?) '''

        self.e_sqlstatement(sqlstatement, parameters)

    def get_lastblock(self):
        '''Getting the last block available in the database'''
        logger.info('Get last blocknumber')
        sqlstatement = '''SELECT max(blocknumber) FROM psale
            UNION
            SELECT max(blocknumber) FROM ssale
            UNION
            SELECT max(blocknumber) FROM nftminted
            UNION
            SELECT max(blocknumber) FROM tinvalidated
            UNION
            SELECT max(blocknumber) FROM tscanned
            ORDER BY max(blocknumber) DESC
            LIMIT 1'''
        c = self.conn.cursor()
        c.execute(sqlstatement)
        block = c.fetchall()[0][0]
        if not block:
            block = 0
        return block
