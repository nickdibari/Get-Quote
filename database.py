#! /usr/bin/python3

# * GetQuote.py                                   * #
# * Nicholas DiBari                               * #
# * --------------------------------------------- * #
# * Provides user interface for Get Quote         * #
# * DataBase Management                           * #
# * --------------------------------------------- * #

import shelve  # DataBase Management


def PrintDB(quotes_DB):
    for key, value in quotes_DB.items():
        print('{0} : '.format(key))
        print(value)
        print('-' * 45)


def DeleteQuote(quotes_DB):
    userDict = {}
    dbKeys = list(quotes_DB.keys())

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
        choice = input('Input not found.\
                       Please enter the number of the quote to delete: ')

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


def SearchQuote(quotes_DB):
    matches = []

    while True:
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

        matches = []  # Reset list
        choice = input('Would you like you search again? (y/n): ')
        if choice == 'n' or choice == 'N':
            break


def Main():
    quotes_DB = shelve.open('.Quotes.db')
    flag = True

    while flag:
        print('Please enter a choice:')
        print('1. Print all Quotes')
        print('2. Delete a Quote')
        print('3. Search for author')
        print('4. [EXIT]')
        choice = input('> ')

        try:
            choice = int(choice)

            # ERROR CHECK
            if choice < 1 or choice > 4:
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

            # [EXIT]
            elif choice == 4:
                flag = False

            # ERROR CHECK
            else:
                print('Sorry that is not a valid input. Try again')

        except ValueError:
            print('Enter in a number silly!')

    quotes_DB.close()


if __name__ == '__main__':
    Main()
