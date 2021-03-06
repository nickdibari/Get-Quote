import os
import sqlite3
import sys
from typing import List, Union


class Quote(object):
    """Represents a row in the quotes table"""

    def __init__(self, id: int, author: str, quote: str, created_at: str):
        self.id = id
        self.author = author
        self.quote = quote
        self.created_at = created_at

    def __str__(self):
        return f'{self.id}  | {self.author}  | {self.quote}  | {self.created_at}'


class DBClient(object):
    """Client for interacting with database for the application"""

    def __init__(self, database_name: str):
        self.conn = self.__connect_to_database(database_name)
        self.__set_up_database(database_name)

    def __execute_query(self, query: str, params: Union[None, tuple] = None) -> sqlite3.Cursor:
        """
        Execute a SQL query using the instance connection to the database

        :param query: (str) SQL statement to execute
        :param params: (None|tuple) Optional params to pass in query

        :return: (sqlite3.Cursor)
        """
        if params is None:
            params = ()

        with self.conn:
            return self.conn.execute(query, params)

    def __connect_to_database(self, database_name: str) -> sqlite3.Connection:
        """
        Open a connection to the sqlite3 database specified by `database_name`.

        :param database_name: (str) Name of sqlite3 database file to open

        :return: (sqlite3.Connection)
        """
        conn = sqlite3.connect(database_name)
        conn.row_factory = sqlite3.Row

        return conn

    def __set_up_database(self, database_name: str) -> None:
        try:
            self.__create_quotes_table()
        except sqlite3.DatabaseError:
            self.__handle_invalid_database_file(database_name)

    def __handle_invalid_database_file(self, database_name: str) -> None:
        """
        If the file specified by `database_name` is not a valid sqlite3 database, prompt
        user to delete the file. If the user allows it, delete the file and create a new
        sqlite3 database file. If the user rejects, exit with error code.

        :param database_name: (str) Name of sqlite3 database file to open
        """
        print(f'ERROR: {database_name} is not a sqlite3 file!')
        delete_file = input('Would you like to delete the old file? (y/n): ')

        if delete_file.lower() == 'y':
            print(f'Deleting {database_name}...')
            os.unlink(database_name)

            print('Creating new database file...')
            self.conn = self.__connect_to_database(database_name)
            self.__set_up_database(database_name)
        else:
            print(
                '\nERROR: Cannot continue with invalid database file.\n'
                'Please delete or rename the file to continue.'
            )
            sys.exit(1)

    def __create_quotes_table(self) -> None:
        """
        Create the table used for storing quotes if it does not exist already
        """
        query = '''
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY,
                author TEXT,
                quote TEXT,
                created_at TEXT
            );
        '''

        self.__execute_query(query)

    def __build_quotes_from_query_result(self, rows: List[sqlite3.Row]) -> List[Quote]:
        """
        Build the list of quote objects returned by a query

        :param rows: (list[sqlite3.Row]) Row objects returned from a query

        :return: (list[Quote])
        """
        quotes = []

        for row in rows:
            quotes.append(Quote(row['id'], row['author'], row['quote'], row['created_at']))

        return quotes

    def close_connection(self) -> None:
        """
        Close connection to the database
        """
        self.conn.close()

    def insert_quote(self, author: str, quote: str, created_at: str) -> None:
        """
        Insert a quote into the database

        :param author: (str) Name of the author that said the quote
        :param quote: (str) The quote for the author
        :param created_at: (str) Timestamp for when the quote was saved to database
        """
        params = (author, quote, created_at)
        query = 'INSERT INTO quotes (author, quote, created_at) VALUES (?, ?, ?)'

        self.__execute_query(query, params)

    def get_all_quotes(self) -> List[Quote]:
        """
        Get all quotes in the database

        :return: (list[Quotes])
        """
        query = '''
            SELECT *
            FROM quotes
            ORDER BY created_at DESC
        '''

        ret = self.__execute_query(query)

        return self.__build_quotes_from_query_result(ret.fetchall())

    def get_quotes_for_author(self, author: str) -> List[Quote]:
        """
        Retrieve quotes from the database for the given author

        :param author: (str) Name of author to retrieve quotes for

        :return: (list[Quotes])
        """
        params = (f'%{author}%',)
        query = '''
            SELECT *
            FROM quotes
            WHERE author LIKE ?
            ORDER BY created_at DESC
        '''

        ret = self.__execute_query(query, params)

        return self.__build_quotes_from_query_result(ret.fetchall())

    def delete_quote_from_database(self, id: int) -> None:
        """
        Delete a quote from the database for the given row

        :param id: (int) Primary key of row to delete from database
        """
        params = (id,)
        query = 'DELETE FROM quotes WHERE id=?'

        self.__execute_query(query, params)
