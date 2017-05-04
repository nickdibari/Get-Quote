#! /usr/bin/python3

#* GetQuote.py                                   *#
#* Nicholas DiBari                               *#
#* --------------------------------------------- *#
#* Provides user interface for Get Quote         *#
#* DataBase Management                           *#
#* --------------------------------------------- *#

import shelve # DataBase Management

#1. Print Quotes
def PrintDB(quotes_DB):
    for key, value in quotes_DB.items():
        print('{0} : '.format(key))
        print(value)
        print('-----------------------------------------------')

#2. Delete Quote
def DeleteQuote(quotes_DB): 
    for key in quotes_DB.keys():
        print(key)
    
    choice=input('Please select the title of the quote to delete: ')
    
    while choice not in list(quotes_DB.keys()):
        choice=input('Input not found. Please enter the title of the quote to delete: ')
        
    #Get quote to delete 
    quote = quotes_DB.get(choice)
    
    #Print quote to delete
    print(choice + ": ")
    print(quote)
    print("-----------------------------------------------")
    confirm = input('Are you sure you want to do delete this quote (y/n): ')

    
    #Delete quote from dictionary
    if confirm == 'y' or confirm == 'Y':
        del quotes_DB[choice]
        print("Deleted\n")

#3. Search Quote
def SearchQuote(quotes_DB):
    matches = [] # list of matched quotes
    
    while True:
        #Get author to search for
        to_search = input("Please enter an author to search for: ")
    
        #Go through list of authors, check if entered author is in any of the previous entries
        for key in quotes_DB.keys():
            if to_search in key:
                matches.append(quotes_DB[key])

        #If no matches, alert user no match was found
        if not matches:
            print("Sorry, did not find " + to_search + " in the database.")
            
        #Else, print matches
        else:
            print("Found the following quotes by " + to_search + ": ")
            print(" ")
            for quote in matches:
                print(quote)
                print("-----------------------------------------------")
        
        matches = [] # Reset list
        choice = input("Would you like you search again? (y/n): ")
        if choice == 'n' or choice == 'N':
            break

#4. Database Management
def DataBaseManager(quotes_DB):
    flag = True
    
    while flag:
        print("Please enter a choice:")
        print("1. Print all Quotes")
        print("2. Delete a Quote")
        print("3. Search for author")
        print("4. [EXIT]")
        choice = input()
        
        try: 
            choice = int(choice)
            
            # ERROR CHECK
            if choice<1 or choice>4:
                print("Sorry that's not a valid choice. Try again")
            
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
                print("Sorry that's not a valid input. Try again")
        
        except ValueError:
            print('Enter in a number silly!')
