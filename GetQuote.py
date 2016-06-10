#! /usr/bin/python3
#* GetQuote.py                                   *#
#* Nicholas DiBari                               *#
#* Prints quote from brainyquote.com from author *# 
#* that user provides                            *#
#* --------------------------------------------- *#
#* Provides user interface for Get Quote         *#
#* DataBase Management                           *#
#* --------------------------------------------- *#

import sys # Get argument
import requests # Get HTML
import bs4 # Parsing HTML
import shelve # Database Management
from datetime import datetime # Date/Time Information

#1. Get name of author to search for
def GetAuthor():
    author = ' '.join(sys.argv[1:])
    print("Searching for " + author + "...")
    return author

#2. Get Quote
def GetQuote(author):
    #Open website with requests 
    HTML = requests.get('http://brainyquote.com/search_results.html?q=' + author )
    HTML.raise_for_status() #Check to ensure page was downloaded correctly

    #Create Beautiful Soup object to parse
    QuoteObject = bs4.BeautifulSoup(HTML.text, "html.parser")

    #Parse Beautiful Soup object for quote
    quotes = QuoteObject.select('.bqQuoteLink a') #Returns the element <a> located within class 'bqQuoteLink'
    return quotes



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
    #Main Loop
    while True:
        # Prompt user to select quote to save
        choice=input("Please pick a quote to save (or enter done to exit): ")
        
        #CASE 1 [EXIT]. Check if user wishes to exit program
        if str(choice) == "done":
            break
        
        #CASE 2 [INPUT ERROR]. Check that number is in rangee
        elif int(choice)<0 or int(choice)>len(quotes):
            print("That is an invalid input. Please enter a number between 0 and " + len(quotes))
            
        #CASE 3 [BASE CASE]. Add selected quote to database
        else:
            DateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Get current date/time
            Author_to_Add = str(author) + " " + DateTime # Get name of author for quote
            Quote_to_Add = str(quotes[int(choice)].getText()) # Get quote to add
            quotes_DB[Author_to_Add] = Quote_to_Add
            print("\nSaved the quote you picked by " + author + ". Good choice\n")

#5. Print Quotes
def PrintDB(quotes_DB):
    #List of keys (Authors)
    keys = list(quotes_DB.keys())
    
    #List of values (Quotes)
    values = list(quotes_DB.values())
    
    #If the two lengths are not the same, trigger Error
    assert len(keys) == len(values)
    
    #Print authors/quotes
    for i in range(len(keys)):
        print(keys[i] + ": ")
        print(values[i])
        print("-----------------------------------------------")

#6. Delete Quote
def DeleteQuote(quotes_DB):
    #List of keys (Authors)
    keys = list(quotes_DB.keys())
    
    #Print list of authors 
    for i in range(len(keys)):
        print(str(i) + ". " + keys[i])
    
    choice=input("Please select the title of the quote to delete: ")
    
    while int(choice)>len(keys) or int(choice)<0:
        choice=input("That is not a valid input. Enter a number between 0 and " + str(len(keys)) + ": ")

    #Get quote to delete 
    quote = quotes_DB.get(keys[int(choice)])
    
    #Print quote to delete
    print("Are you sure you want to do delete the following quote (y/n): ")
    print(keys[int(choice)] + ": ")
    print(quote)
    print("-----------------------------------------------")
    confirm = input()
    
    #Delete quote from dictionary
    if confirm == 'y' or confirm == 'Y':
        del quotes_DB[keys[int(choice)]]
        print("Deleted\n")

#7. Search Quote
def SearchQuote(quotes_DB):
    matches = [] # list of matched quotes
    authors = list(quotes_DB.keys()) #Get list of authors
    quotes = list(quotes_DB.values()) #Get list of aquotes
    
    #Main Loop
    while True:
        #Get author to search for
        to_search = input("Please enter an author to search for: ")
    
        #Go through list of authors, check if entered author is in any of the previous entries
        for i in range(len(authors)):
            if to_search in authors[i]:
                matches.append(quotes[i])

        #If no matches, alert user no match was found
        if not matches:
            print("Sorry, did not find " + to_search + " in the database.")
            
        #Else, print matches
        else:
            print("Found the following quotes by " + to_search + ": ")
            print(" ")
            for j in range(len(matches)):
                print (matches[j])
                print("-----------------------------------------------")
        
        matches = [] # Reset list
        choice = input("Would you like you search again? (y/n): ")
        if choice == 'n' or choice == 'N':
            break

#8. Database Management
def DataBase_Manager(quotes_DB):
    while True:
        print("Please enter a choice:")
        print("1. Print all Quotes")
        print("2. Delete a Quote")
        print("3. Search for author")
        print("4. [EXIT]")
        choice = input()
        
        # ERROR CHECK
        if int(choice)<1 or int(choice)>4:
            print("Sorry that's not a valid choice. Try again")
        
        # PRINT QUOTES
        elif int(choice) == 1:
            PrintDB(quotes_DB)
        
        # DELETE QUOTE
        elif int(choice) == 2:
            DeleteQuote(quotes_DB)
        
        # SEARCH QUOTE
        elif int(choice) == 3:
            SearchQuote(quotes_DB)
        
        # [EXIT]
        elif int(choice) == 4:
            exit(0)
        
        # ERROR CHECK
        else:
            print("Sorry that's not a valid input. Try again")
        
    
#Main Function
def Main():
    #Database Declaration
    quotes_DB=shelve.open('.Quotes.db')
    author = " " # Author to search for
    quotes = [] # List of quotes returned
       
    #ERROR: NO ARGS
    if len(sys.argv) == 1:
        print("ERROR: Enter -h or -help for help")
        exit(1)
    
    #Help 
    if sys.argv[1] == '-h' or sys.argv[1] == '-help':
        print("GET_QUOTE.PY")
        print("1) Get_Quote.py AUTHOR")
        print("   Usage: Return first 10 quotes from author found on\nbrainyquote.com")
        print("2) Getquote.py -d [or -D]")
        print("   Usage: Database Management for Get_Quote Program")
        exit(0)
        
    #Database Management
    if sys.argv[1] == '-d' or sys.argv[1] == '-D':
        DataBase_Manager(quotes_DB)
    
    #Search Option
    else:
        author = GetAuthor()
        quotes = GetQuote(author)
        PrintQuotes(quotes, author)
        SaveQuote(quotes_DB, quotes, author)
    
    print("Goodbye!")   
    quotes_DB.close() # Close Database
    
    

Main()
