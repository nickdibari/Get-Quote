# Get-Quote
OVERVIEW:
      Python program to scrape brainyquote.com for quotes from a user entered author
      
      Also contains a DataBase feature to store and search for previously viewed quotes
      
      REQUIRES BeautifulSoup4 and Shelve to work
      
      Will create a file in directory named .Quotes.db

USAGE:

            ./Get_Quote.py AUTHOR
                  Returns 10 quotes from brainyquote.com that match author user provides
                  Prompts user if they want to save any quotes into DataBase
            
            ./Get_Quote.py -d [or -D]
                  DataBase Manager for storing previously searched quotes
            
            ./Get_Quote.py -h [or -help]
                  Displays the different usages 
