#! /usr/bin/python3

# * database.py                                   * #
# * Nicholas DiBari                               * #
# * --------------------------------------------- * #
# * Provides user interface for Get Quote         * #
# * DataBase Management                           * #
# * --------------------------------------------- * #

import argparse
import sys
import shelve


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


def print_quotes(quotes_db):
    """
    Print all quotes from the database
    """
    for key, value in quotes_db.items():
        print('{}: '.format(key))
        print(value)
        print('-' * 45)
    else:
        print('Your database is empty!')


def delete_quotes(quotes_db):
    """
    Delete a specific quote from the database
    TODO: Add option to send author name to function as kwarg
    """
    user_dict = {}
    db_keys = list(quotes_db.keys())

    # Creates a dict of quoteDB keys as values with easier to enter
    # keys mapped to them
    for i in range(len(db_keys)):
        user_dict[str(i)] = db_keys[i]

    user_keys = [int(x) for x in list(user_dict.keys())]
    user_keys.sort()

    print('Num | Author')
    print('-' * 45)
    for key in user_keys:
        title = user_dict.get(str(key))
        print('{}: {}'.format(key, title))

    choice = input('Please select the number of the quote to delete: ')

    while choice not in user_dict.keys():
        print('Input not found')
        choice = input('Please select the number of the quote to delete: ')

    # Get quote to delete
    quote_key = user_dict.get(choice)
    quote = quotes_db.get(quote_key)

    # Print quote to delete
    print('{}: '.format(quote_key))
    print(quote)
    print('-' * 45)
    confirm = input('Are you sure you want to delete this quote (y/n): ')

    if confirm.lower() == 'y':
        del quotes_db[quote_key]
        print('Deleted quote {}'.format(quote_key))


def search_quotes(quotes_db, to_search=None):
    """
    Search database for all quotes from an author and write them to the console

    :param quotes_db: (shelve.DbfilenameShelf) Connection to shelve database file
    :param to_search: Name of author to search database for matching quotes
    """
    matches = []
    flag = False

    if to_search:
        flag = True  # Account for search argument from command line

    while True:
        if not to_search:
            to_search = input('Please enter an author to search for: ')

        for key in quotes_db.keys():
            if to_search in key:
                matches.append(quotes_db[key])

        if not matches:
            print('Sorry, did not find {} in the database.'.format(to_search))

        else:
            print('Found the following quotes by {}'.format(to_search))
            print('-' * 45)
            for quote in matches:
                print(quote)
                print('-' * 45)

        if flag:
            break

        matches = []  # Reset list
        choice = input('Would you like you search again? (y/n): ')

        if choice.lower() == 'n':
            break
        else:
            to_search = None


def dump_quotes(quotes_db, file_name=None):
    """
    Write all quotes in the database to a text file

    :param quotes_db: (shelve.DbfilenameShelf) Connection to shelve database file
    :param file_name: (str) Name of file to write data
    """
    if not file_name:
        file_name = input('Please enter the filename to save the quotes to: ')

    if not file_name.endswith('.txt'):
        file_name += '.txt'

    with open(file_name, 'w') as f:
        for key, value in quotes_db.items():
            f.write('{0}: {1}\n'.format(key, value))
            f.write('-' * 90 + '\n')

    print('Done! Your quotes can be found in {}'.format(file_name))


def interactive_mode(quotes_db):
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
                print_quotes(quotes_db)

            # DELETE QUOTE
            elif choice == 2:
                delete_quotes(quotes_db)

            # SEARCH QUOTE
            elif choice == 3:
                search_quotes(quotes_db)

            # DUMP DATABASE
            elif choice == 4:
                dump_quotes(quotes_db)

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
    quotes_db = shelve.open('.Quotes.db')

    parser = create_arg_parser()
    args = parser.parse_args(sys.argv[1:])

    if args.interactive_mode:
        interactive_mode(quotes_db)

    elif args.print_db:
        print_quotes(quotes_db)

    elif args.author:
        search_quotes(quotes_db, to_search=args.author)

    elif args.delete:
        delete_quotes(quotes_db)

    elif args.output_file:
        dump_quotes(quotes_db, file_name=args.output_file)

    else:
        parser.print_help()

    quotes_db.close()


if __name__ == '__main__':
    main()
