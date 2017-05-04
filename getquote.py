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
from datetime import datetime # Date/Time Information

from database import DataBase_Manager

#1. Get name of author to search for
def GetAuthor():
    author = ' '.join(sys.argv[1:])
    print("Searching for " + author + "...")
    return author

#2. Get Quote
def GetQuote(author):
    results = []

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
def PrintQuotes(quotes, author):
    #Get number of quotes to print. I didn't want to print all of the quotes, so I set the max allowed to print
    #to 10
    num_quotes = min(10, len(quotes))

    #Print all quotes retrievd
    print(" ")
    print("Found the following matches for " + author + ":")
    print("-----------------------------------------------")
    for i in range(num_quotes):
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
       
    #ERROR: NO ARGS
    if len(sys.argv) == 1:
        print("ERROR: Enter -h or --help for help")
        exit(1)
    
    #Help 
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print("GET_QUOTE.PY")
        print("1) getquote.py AUTHOR")
        print("   Usage: Return first 10 quotes from author found on\nbrainyquote.com")
        print("2) getquote.py -d [or --database]")
        print("   Usage: Database Management for getquote Program")
        exit(0)
        
    #Database Management
    if sys.argv[1] == '-d' or sys.argv[1] == '--database':
        DataBase_Manager(quotes_DB)
    
    #Search Option
    else:
        author = GetAuthor()
        quotes = GetQuote(author)
        PrintQuotes(quotes, author)
        SaveQuote(quotes_DB, quotes, author)
    
    print("Goodbye!")   
    quotes_DB.close() # Close Database

if __name__ == '__main__':
    Main()
