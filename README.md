# Get-Quote

## Overview
Python program to scrape brainyquote.com for quotes from a user entered author. Also contains a DataBase feature to store and search for previously viewed quotes

Will create a file in the current directory for storing saved quotes. This will be set to the value of the
`DB_NAME` variable defined in the `settings.py` file.

## Requirements
* [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4)
* [Shelve](https://docs.python.org/2/library/shelve.html)

## Usage
### getquote

Script to retrieve quotes for a given author

```
./getquote.py AUTHOR [options]

positional arguments:
  AUTHOR         Search for quotes from AUTHOR

optional arguments:
  -h, --help     show this help message and exit
  -n NUM_QUOTES  Number of quotes to retrieve (default 10)
  --print        Set to just print quotes retrieved to console
```
### database

Interactive script to interact with stored database of quotes

```
./database.py [-i --interactive] [-p --print] [-s --search <author>] [-d --delete] [--dump <output file>]

optional arguments:
  -h, --help            show this help message and exit
  -i, --interactive     Open your database interface
  -p, --print           Print all quotes from your database
  -s AUTHOR, --search AUTHOR
                        Search your database for quotes matching author
  -d, --delete          Run delete interface to remove quotes from your
                        database
  --dump OUTPUT_FILE    Save contents of your database to a text file.
```

## License
MIT license, see License
