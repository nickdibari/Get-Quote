# Get-Quote

## Overview
Python program to scrape brainyquote.com for quotes from a user entered author. Also contains a DataBase feature to store and search for previously viewed quotes

Will create a file in directory named .Quotes.db

## Requirements
* [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4)
* [Shelve](https://docs.python.org/2/library/shelve.html)

## Usage
 ```
./getquote.py AUTHOR
```
Returns 10 quotes from brainyquote.com that match author user provides
Prompts user if they want to save any quotes into DataBase

```
./getquote.py -d [or --database]
``` 
DataBase Manager for storing previously searched quotes

```
./getquote.py -h [or --help]
```
Displays the different usages 

## License
MIT license, see License
