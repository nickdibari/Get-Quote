#! /usr/bin/python3

# * get_quotes.py                                   * #
# * Nicholas DiBari                               * #
# * --------------------------------------------- * #
# * Prints quote from brainyquote.com from author * #
# * that user provides                            * #
# * --------------------------------------------- * #

import argparse  # Command line argument parsing
import sys  # Get argument
from datetime import datetime  # Date/Time Information

import requests  # Get HTML
import bs4  # Parsing HTM

import settings
from utils import DBClient


def create_arg_parser():
    description = 'The Easy to use Quote Search'

    parser = argparse.ArgumentParser(
        prog='./getquote.py',
        usage='%(prog)s AUTHOR [options]',
        description=description
    )

    parser.add_argument(
        'author',
        metavar='AUTHOR',
        nargs='*',
        help='Search for quotes from AUTHOR'
    )

    parser.add_argument(
        '-n',
        action='store',
        type=int,
        default=10,
        dest='num_quotes',
        help='Number of quotes to retrieve (default %(default)s)'
    )

    parser.add_argument(
        '--print',
        action='store_true',
        default=False,
        dest='print',
        help='Set to just print quotes retrieved to console'
    )

    return parser


def get_quotes(author, num_quotes):
    results = []

    print('Searching for {}...'.format(author))

    # Open website with requests
    response = requests.get('https://brainyquote.com/search_results?q={}'.format(author))
    response.raise_for_status()  # Check to ensure page was downloaded OK

    # Create Beautiful Soup object to parse
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    # Parse Beautiful Soup object for quote
    quotes = soup.select('#quotesList a')

    for quote in quotes:
        if quote.get('title') == 'view quote' and len(results) < num_quotes:
            results.append(quote)

    return results


def print_quotes(quotes, author):
    print('Found the following matches for {}'.format(author))
    print('-' * 45)

    for idx, quote in enumerate(quotes):
        print('{}. {}'.format(idx, quote.getText().strip()))
        print('-' * 45)


def save_quotes(db_client, quotes, author):
    while True:
        choice = input('Please pick a quote to save (or enter done to exit): ')

        # CASE 1 [EXIT]. Check if user wishes to exit program
        if choice == 'done':
            break

        else:
            try:
                choice = int(choice)

                # CASE 2 [INPUT ERROR]. Check that number is in range
                if choice < 0 or choice > len(quotes):
                    print('That is an invalid input. Please enter a number between 0 and {}'.format(len(quotes)))

                # CASE 3 [BASE CASE]. Add selected quote to database
                else:
                    created_at = datetime.now().isoformat()
                    quote = quotes[choice].getText().strip()
                    db_client.insert_quote(author, quote, created_at)

                    print('Saved the quote you picked by {}. Good choice!'.format(author))

            except ValueError:
                print('Enter in a number silly!')


def main():
    db_client = DBClient(settings.DB_NAME)

    parser = create_arg_parser()
    args = parser.parse_args(sys.argv[1:])

    author = ' '.join(args.author)
    num_quotes = args.num_quotes

    # Account for empty string
    if author == '':
        parser.print_help()

    else:
        quotes = get_quotes(author, num_quotes)
        print_quotes(quotes, author)

        if not args.print:
            save_quotes(db_client, quotes, author)

    db_client.close_connection()


if __name__ == '__main__':
    main()
