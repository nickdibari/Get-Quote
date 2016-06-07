# Get-Quote

## Overview
      Python program to scrape brainyquote.com for quotes from a user entered author. Also contains a DataBase feature to store and search for previously viewed quotes
      
      REQUIRES BeautifulSoup4 and Shelve to work
      
      Will create a file in directory named .Quotes.db

## Usage
 ```
./GetQuote.py AUTHOR
```
Returns 10 quotes from brainyquote.com that match author user provides
Prompts user if they want to save any quotes into DataBase

```
./GetQuote.py -d
``` 
DataBase Manager for storing previously searched quotes

```
./GetQuote.py -h [or -help]
```
Displays the different usages 

## License
MIT license, see License
