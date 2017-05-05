# Get-Quote

## Overview
Python program to scrape brainyquote.com for quotes from a user entered author. Also contains a DataBase feature to store and search for previously viewed quotes

Will create a file in directory named .Quotes.db

## Requirements
* [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4)
* [Shelve](https://docs.python.org/2/library/shelve.html)

## Usage
### getquote

Script to retrieve quotes for a given author

```
./getquote.py AUTHOR [-n NUMQUOTES] [-q or --quiet] [-h or --help]

positional arguments:
  AUTHOR        Search for quotes from AUTHOR

optional arguments:
  -h, --help    show this help message
  -n NUMQUOTES  will print NUMQUOTES number of retrieved quotes (default 10)
  -q, --quiet   set to ignore saving quotes to DB
```
### database

Interactive script to interact with stored database of quotes

```
./database.py
```

## License
MIT license, see License
