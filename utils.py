import sqlite3
import shelve
from typing import List


def connect_db(name):
    """
    Open a connection to the database used to store quotes.

    :param name: (str) Name of database file

    :return: (shelve.DbfilenameShelf)
    """
    try:
        return shelve.open(name)
    except Exception:
        raise Exception('Unable to connect to database with name {}'.format(name))


class Quote(object):
    """Represents a row in the quotes table"""

    def __init__(self, id: int, author: str, quote: str, created_at: str):
        self.id = id
        self.author = author
        self.quote = quote
        self.created_at = created_at


class DBClient(object):
    """Client for interacting with database for the application"""

    def __init__(self, database_name: str):
        self.conn = sqlite3.connect(database_name)
        self.conn.row_factory = sqlite3.Row
        self._create_quotes_table()

    def _create_quotes_table(self):
        """
        Create the table used for storing quotes if it does not exist already
        """
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS quotes (
                    id INTEGER PRIMARY KEY,
                    author TEXT,
                    quote TEXT,
                    created_at TEXT
                );
            ''')

    def close_connection(self):
        """
        Close connection to the database
        """
        self.conn.close()

    def insert_quote(self, author: str, quote: str, created_at: str):
        """
        Insert a quote into the database

        :param author: (str) Name of the author that said the quote
        :param quote: (str) The quote for the author
        :param created_at: (str) Timestamp for when the quote was saved to database
        """
        with self.conn:
            self.conn.execute('''
                INSERT INTO quotes (author, quote, created_at) VALUES (?, ?, ?)
            ''', (author, quote, created_at))

    def get_quotes_for_author(self, author: str) -> List[Quote]:
        """
        Retrieve quotes from the database for the given author

        :param author: (str) Name of author to retrieve quotes for

        :return: (list[Quotes])
        """
        quotes = []

        with self.conn:
            ret = self.conn.execute('''
                SELECT *
                FROM quotes
                WHERE author=?
            ''', (author,))

        # Build list of quote objects for return value
        for row in ret.fetchall():
            quotes.append(Quote(row['id'], row['author'], row['quote'], row['created_at']))

        return quotes
