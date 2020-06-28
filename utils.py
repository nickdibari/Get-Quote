import shelve


def connect_db(name):
    """
    Open a connection to the database used to store quotes.

    :param name: (str) Name of database file

    :return: (shelve.DbfilenameShelf)
    """
    try:
        return shelve.open(name)
    except Exception:
        raise Exception('Unable to connect to database with name {}'.format(name))
