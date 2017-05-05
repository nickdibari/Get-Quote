#! /usr/bin/python3

# * GetQuote.py                                   * #
# * Nicholas DiBari                               * #
# * --------------------------------------------- * #
# * Prints quote from brainyquote.com from author * #
# * that user provides                            * #
# * --------------------------------------------- * #

import sys  # Get argument
import requests  # Get HTML
import bs4  # Parsing HTML
import shelve  # Database Management
import argparse  # Command line argument parsing
from datetime import datetime  # Date/Time Information


def ArgParser():
    description = 'The Easy to use Quote Search'

    parser = argparse.ArgumentParser(prog='./getquote.py',
                                     usage='%(prog)s AUTHOR [options]',
                                     description=description)

    parser.add_argument('author', metavar='AUTHOR', nargs='*',
                        help='Search for quotes from AUTHOR')

    parser.add_argument('-n', action='store', type=int, default=10,
                        dest='numQuotes',
                        help='will print NUMQUOTES number of retrieved quotes\
                             (default 10)')

    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        dest='quiet', help='set to ignore saving quotes to DB')

    return parser


def GetQuote(author):
    results = []

    print('Searching for {}...'.format(author))

    # Open website with requests
    response = requests.get('http://brainyquote.com/search_results.html?q={}'
                            .format(author))
    response.raise_for_status()  # Check to ensure page was downloaded OK

    # Create Beautiful Soup object to parse
    QuoteObject = bs4.BeautifulSoup(response.text, 'html.parser')

    # Parse Beautiful Soup object for quote
    quotes = QuoteObject.select('#quotesList a')

    for quote in quotes:
        if quote.get('title') == 'view quote':
            results.append(quote)

    return results


def PrintQuotes(quotes, author, numQuotes):
    if numQuotes > len(quotes):
        numQuotes = len(quotes)

    print('Found the following matches for {}'.format(author))
    print('-' * 45)

    for i in range(numQuotes):
        print('{0}. {1}'.format(str(i), quotes[i].getText()))
        print('-' * 45)


def SaveQuote(quotes_DB, quotes, author):
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
                    print('That is an invalid input.\
                          Please enter a number between 0 and {}'
                          .format(len(quotes)))

                # CASE 3 [BASE CASE]. Add selected quote to database
                else:
                    DateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    Author_to_Add = '{0} {1}'.format(author, DateTime)
                    Quote_to_Add = quotes[choice].getText()
                    quotes_DB[Author_to_Add] = Quote_to_Add

                    print('Saved the quote you picked by {}. Good choice'
                          .format(author))

            except ValueError:
                print('Enter in a number silly!')


def Main():
    quotes_DB = shelve.open('.Quotes.db')

    parser = ArgParser()
    args = parser.parse_args(sys.argv[1:])

    author = ' '.join(args.author)
    numQuotes = args.numQuotes

    # Account for empty string
    if author == '':
        parser.print_help()

    else:
        quotes = GetQuote(author)
        PrintQuotes(quotes, author, numQuotes)

        if not args.quiet:
            SaveQuote(quotes_DB, quotes, author)

        print('Goodbye!')

    quotes_DB.close()


if __name__ == '__main__':
    Main()
