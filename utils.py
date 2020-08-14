import sqlite3
from typing import List


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

    def _build_quotes_from_query_result(self, rows: List[sqlite3.Row]) -> List[Quote]:
        """
        Build the list of quote objects returned by a query

        :param rows: (list[sqlite3.Row]) Row objects returned from a query

        :return: (list[Quote])
        """
        quotes = []

        for row in rows:
            quotes.append(Quote(row['id'], row['author'], row['quote'], row['created_at']))

        return quotes

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

    def get_all_quotes(self) -> List[Quote]:
        """
        Get all quotes in the database
        """
        with self.conn:
            ret = self.conn.execute('''
                SELECT *
                FROM quotes
                ORDER BY created_at DESC
            ''')

        return self._build_quotes_from_query_result(ret.fetchall())

    def get_quotes_for_author(self, author: str) -> List[Quote]:
        """
        Retrieve quotes from the database for the given author

        :param author: (str) Name of author to retrieve quotes for

        :return: (list[Quotes])
        """
        with self.conn:
            ret = self.conn.execute('''
                SELECT *
                FROM quotes
                WHERE author LIKE ?
                ORDER BY created_at DESC
            ''', (f'%{author}%',))

        return self._build_quotes_from_query_result(ret.fetchall())

    def delete_quote_from_database(self, id: int):
        """
        Delete a quote from the database for the given row

        :param id: (int) Primary key of row to delete from database
        """
        with self.conn:
            self.conn.execute('''
                DELETE FROM quotes
                WHERE id=?
            ''', (id,))
