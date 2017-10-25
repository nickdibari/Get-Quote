#! /usr/bin/python3

# * GetQuote.py                                   * #
# * Nicholas DiBari                               * #
# * --------------------------------------------- * #
# * Provides user interface for Get Quote         * #
# * DataBase Management                           * #
# * --------------------------------------------- * #

import argparse
import sys
import shelve


def ArgParser():
    """
    Create parser for command line arguments
    - Return an ArgumentParser object that will determine what function to run
    """
    prog = './database.py'
    usage = '{} [-i --interactive] [-p --print] [-s --search <author>]\
            [-d --delete] [--dump <output file>]'
    description = 'The Easy to use Database Manager'

    parser = argparse.ArgumentParser(
        prog=prog,
        usage=usage.format(prog),
        description=description
    )

    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        default=False,
        dest='interactive_mode',
        help='Open your database interface'
    )

    parser.add_argument(
        '-p', '--print',
        action='store_true',
        default=False,
        dest='print_db',
        help='Print all quotes from your database'
    )

    parser.add_argument(
        '-s', '--search',
        action='store',
        type=str,
        default='',
        dest='author',
        help='Search your database for quotes matching author'
    )

    parser.add_argument(
        '-d', '--delete',
        action='store_true',
        default=False,
        dest='delete',
        help='Run delete interface to remove quotes from your database')

    parser.add_argument(
        '--dump',
        action='store',
        type=str,
        default='',
        dest='output_file',
        help='Save contents of your database to a text file.')

    return parser


def PrintDB(quotes_DB):
    """
    Print all quotes from the database
    """
    for key, value in quotes_DB.items():
        print('{0} : '.format(key))
        print(value)
        print('-' * 45)


def DeleteQuote(quotes_DB):
    """
    Delete a specific quote from the database
    TODO: Add option to send author name to function as kwarg
    """
    userDict = {}
    dbKeys = list(quotes_DB.keys())

    # Creates a dict of quoteDB keys as values with easier to enter
    # keys mapped to them
    for i in range(len(dbKeys)):
        userDict[str(i)] = dbKeys[i]

    userKeys = [int(x) for x in list(userDict.keys())]
    userKeys.sort()

    print('Num | Author/Datetime Stamp')
    print('-' * 45)
    for key in userKeys:
        title = userDict.get(str(key))
        print('{0}: {1}'.format(key, title))

    choice = input('Please select the number of the quote to delete: ')

    while choice not in userDict.keys():
        print('Input not found.')
        choice = input('Please select the number of the quote to delete: ')

    # Get quote to delete
    quoteKey = userDict.get(choice)
    quote = quotes_DB.get(quoteKey)

    # Print quote to delete
    print('{}: '.format(quoteKey))
    print(quote)
    print('-' * 45)
    confirm = input('Are you sure you want to delete this quote (y/n): ')

    if confirm == 'y' or confirm == 'Y':
        del quotes_DB[quoteKey]
        print('Deleted\n')


def SearchQuote(quotes_DB, to_search=None):
    """
    Search database for all quotes from an author
    - to_search: Optional kwarg, used for command line interface
    """
    matches = []
    flag = False

    if to_search:
        flag = True  # Account for search argument from command line

    while True:
        if not to_search:
            to_search = input('Please enter an author to search for: ')

        for key in quotes_DB.keys():
            if to_search in key:
                matches.append(quotes_DB[key])

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
        if choice == 'n' or choice == 'N':
            break


def DumpQuotes(quotes_DB, fileName=None):
    """
    Save all quotes to a text file
    fileName: Optional kwarg, used for command line interface
    """
    if not fileName:
        fileName = input('Please enter the filename to save the quotes to: ')

    if not fileName.endswith('.txt'):
        fileName += '.txt'

    with open(fileName, 'w') as f:
        for key, value in quotes_DB.items():
            f.write('{0}: {1}\n'.format(key, value))
            f.write('-' * 90 + '\n')

    print('Done! Your quotes can be found in {}'.format(fileName))


def InterActiveMode(quotes_DB):
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
                PrintDB(quotes_DB)

            # DELETE QUOTE
            elif choice == 2:
                DeleteQuote(quotes_DB)

            # SEARCH QUOTE
            elif choice == 3:
                SearchQuote(quotes_DB)

            # DUMP DATABASE
            elif choice == 4:
                DumpQuotes(quotes_DB)

            # [EXIT]
            elif choice == 5:
                flag = False

            # ERROR CHECK
            else:
                print('Sorry that is not a valid input. Try again')

        except ValueError:
            print('Enter in a number silly!')


def Main():
    """
    Driver function for script
    Determines to run interactive shell or to call specific function using
    command line arguments
    """
    quotes_DB = shelve.open('.Quotes.db')

    parser = ArgParser()
    args = parser.parse_args(sys.argv[1:])

    if args.interactive_mode:
        InterActiveMode(quotes_DB)

    elif args.print_db:
        PrintDB(quotes_DB)

    elif args.author:
        SearchQuote(quotes_DB, to_search=args.author)

    elif args.delete:
        DeleteQuote(quotes_DB)

    elif args.output_file:
        DumpQuotes(quotes_DB, fileName=args.output_file)

    else:
        parser.print_help()

    quotes_DB.close()


if __name__ == '__main__':
    Main()
