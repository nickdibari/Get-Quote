#! /usr/bin/python3

# * database.py                                   * #
# * Nicholas DiBari                               * #
# * --------------------------------------------- * #
# * Provides user interface for Get Quote         * #
# * DataBase Management                           * #
# * --------------------------------------------- * #

import argparse
import sys

import settings
from utils import DBClient


def create_arg_parser():
    """
    Create parser for command line arguments
    - Return an ArgumentParser object that will determine what function to run
    """
    description = 'The Easy to use Database Manager'

    parser = argparse.ArgumentParser(
        prog='./database.py',
        usage='%(prog)s [-i --interactive] [-p --print] [-s --search <author>] [-d --delete] [--dump <output file>]',
        description=description
    )

    parser.add_argument(
        '-i',
        '--interactive',
        action='store_true',
        default=False,
        dest='interactive_mode',
        help='Open your database interface'
    )

    parser.add_argument(
        '-p',
        '--print',
        action='store_true',
        default=False,
        dest='print_db',
        help='Print all quotes from your database'
    )

    parser.add_argument(
        '-s',
        '--search',
        action='store',
        type=str,
        default='',
        dest='author',
        help='Search your database for quotes matching author'
    )

    parser.add_argument(
        '-d',
        '--delete',
        action='store_true',
        default=False,
        dest='delete',
        help='Run delete interface to remove quotes from your database'
    )

    parser.add_argument(
        '--dump',
        action='store',
        type=str,
        default='',
        dest='output_file',
        help='Save contents of your database to a text file.'
    )

    return parser


def print_quotes(db_client):
    """
    Print all quotes from the database
    """
    quotes = db_client.get_all_quotes()

    if not quotes:
        print('Your database is empty!')
        return

    for quote in quotes:
        print('{}: {} | {} | {}'.format(quote.id, quote.author, quote.quote, quote.created_at))
        print('-' * 45)


def delete_quotes(db_client):
    """
    Delete a specific quote from the database
    TODO: Add option to send author name to function as kwarg
    """
    quotes = db_client.get_all_quotes()

    print('Num | Author')
    print('-' * 45)
    for quote in quotes:
        print('{}: {}'.format(quote.id, quote.author))

    choice = input('Please select the number of the quote to delete: ')
    confirm = input('Are you sure you want to delete this quote (y/n): ')

    if confirm.lower() == 'y':
        db_client.delete_quote_from_database(choice)
        print('Deleted quote {}'.format(choice))


def search_quotes(db_client, to_search=None):
    """
    Search database for all quotes from an author and write them to the console

    :param db_client: (DBClient) Connection to database
    :param to_search: Name of author to search database for matching quotes
    """
    flag = False

    if to_search:
        flag = True  # Account for search argument from command line

    while True:
        if not to_search:
            to_search = input('Please enter an author to search for: ')

        quotes = db_client.get_quotes_for_author(to_search)

        if not quotes:
            print('Sorry, did not find {} in the database.'.format(to_search))

        else:
            print('Found the following quotes by {}'.format(to_search))
            print('-' * 45)
            for quote in quotes:
                print('{}: {} | {} | {}'.format(quote.id, quote.author, quote.quote, quote.created_at))
                print('-' * 45)

        if flag:
            break

        choice = input('Would you like you search again? (y/n): ')

        if choice.lower() == 'n':
            break
        else:
            to_search = None


def dump_quotes(db_client, file_name=None):
    """
    Write all quotes in the database to a text file

    :param db_client: (DBClient) Connection to database
    :param file_name: (str) Name of file to write data
    """
    if not file_name:
        file_name = input('Please enter the filename to save the quotes to: ')

    if not file_name.endswith('.txt'):
        file_name += '.txt'

    with open(file_name, 'w') as f:
        for quote in db_client.get_all_quotes():
            f.write('{0}: {1}\n'.format(quote.author, quote.quote))
            f.write('-' * 90 + '\n')

    print('Done! Your quotes can be found in {}'.format(file_name))


def interactive_mode(db_client):
    """
    Loop to run the functionality in a shell-like mode
    """
    flag = True

    while flag:
        print('Please enter a choice:')
        print('1. Print all Quotes')
        print('2. Delete a Quote')
        print('3. Search for author')
        print('4. Dump Database to text file')
        print('5. [EXIT]')
        choice = input('> ')

        try:
            choice = int(choice)

            # ERROR CHECK
            if choice < 1 or choice > 5:
                print('Sorry that is not a valid choice. Try again')

            # PRINT QUOTES
            elif choice == 1:
                print_quotes(db_client)

            # DELETE QUOTE
            elif choice == 2:
                delete_quotes(db_client)

            # SEARCH QUOTE
            elif choice == 3:
                search_quotes(db_client)

            # DUMP DATABASE
            elif choice == 4:
                dump_quotes(db_client)

            # [EXIT]
            elif choice == 5:
                flag = False

            # ERROR CHECK
            else:
                print('Sorry that is not a valid input. Try again')

        except ValueError:
            print('Enter in a number silly!')


def main():
    """
    Driver function for script
    Determines to run interactive shell or to call specific function using
    command line arguments
    """
    db_client = DBClient(settings.DB_NAME)

    parser = create_arg_parser()
    args = parser.parse_args(sys.argv[1:])

    if args.interactive_mode:
        interactive_mode(db_client)

    elif args.print_db:
        print_quotes(db_client)

    elif args.author:
        search_quotes(db_client, to_search=args.author)

    elif args.delete:
        delete_quotes(db_client)

    elif args.output_file:
        dump_quotes(db_client, file_name=args.output_file)

    else:
        parser.print_help()

    db_client.close_connection()


if __name__ == '__main__':
    main()
