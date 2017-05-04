#! /usr/bin/python3

#* GetQuote.py                                   *#
#* Nicholas DiBari                               *#
#* --------------------------------------------- *#
#* Prints quote from brainyquote.com from author *# 
#* that user provides                            *#
#* --------------------------------------------- *#

import sys # Get argument
import requests # Get HTML
import bs4 # Parsing HTML
import shelve # Database Management
import argparse # Command line argument parsing
from datetime import datetime # Date/Time Information

from database import DataBaseManager

#1. Arg Parser Definition
def ArgParser():
    parser = argparse.ArgumentParser(prog='./getquote', usage='%(prog)s AUTHOR [options]',
                                     description='The easy to use Quote Finder')

    parser.add_argument('author', metavar='AUTHOR', nargs='*', help='Search for quotes from AUTHOR')
    parser.add_argument('-n', action='store', type=int, default=10, dest='numQuotes', help='Will print N number of retrieved quotes (default 10)')

    return parser

#2. Get Quote
def GetQuote(author):
    results = []

    print('Searching for {}...'.format(author))

    #Open website with requests 
    HTML = requests.get('http://brainyquote.com/search_results.html?q=' + author )
    HTML.raise_for_status() #Check to ensure page was downloaded correctly

    #Create Beautiful Soup object to parse
    QuoteObject = bs4.BeautifulSoup(HTML.text, "html.parser")

    #Parse Beautiful Soup object for quote
    quotes = QuoteObject.select('#quotesList a') #Returns the element <a> located within class 'quotesList'

    for quote in quotes:
      if quote.get('title') == 'view quote':
          results.append(quote)

    return results

#3. Print Quote
def PrintQuotes(quotes, author, numQuotes):

    #Print all quotes retrievd
    print(" ")
    print("Found the following matches for " + author + ":")
    print("-----------------------------------------------")
    for i in range(numQuotes):
        print(str(i) + ". " + quotes[i].getText())
        print(' ')

#4. Save Quote
def SaveQuote(quotes_DB, quotes, author):  
    
    while True:
        choice=input("Please pick a quote to save (or enter done to exit): ")
        
        #CASE 1 [EXIT]. Check if user wishes to exit program
        if choice == "done":
            break
        
        else:
            try:
                choice = int(choice)

                #CASE 2 [INPUT ERROR]. Check that number is in rangee
                if choice<0 or choice>len(quotes):
                    print("That is an invalid input. Please enter a number between 0 and " + len(quotes))

                #CASE 3 [BASE CASE]. Add selected quote to database
                else:
                    DateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Get current date/time
                    Author_to_Add = str(author) + " " + DateTime # Get name of author for quote
                    Quote_to_Add = str(quotes[int(choice)].getText()) # Get quote to add
                    quotes_DB[Author_to_Add] = Quote_to_Add
                    print("Saved the quote you picked by " + author + ". Good choice")

            except ValueError:
                print('Enter in a number silly!')
    
#Main Function
def Main():
    quotes_DB=shelve.open('.Quotes.db')

    parser = ArgParser()
    args = parser.parse_args(sys.argv[1:])
    
    author = ' '.join(args.author)
    numQuotes = args.numQuotes

    quotes = GetQuote(author)
    PrintQuotes(quotes, author, numQuotes)
    SaveQuote(quotes_DB, quotes, author)

    print("Goodbye!")
    quotes_DB.close() # Close Database

if __name__ == '__main__':
    Main()
