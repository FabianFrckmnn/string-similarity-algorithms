"""
MongoDB Connection Utility

This module provides utility functions for loading environment variables and connecting
to a MongoDB database using the connection string defined in the environment. It relies
on the `dotenv` package to read environment variables from a `.env` file and the `pymongo`
package to establish the database connection.

Functions
---------
__load_env()
    Loads environment variables from a `.env` file using the `dotenv` package.
connect()
    Establishes a connection to the MongoDB database using the connection string found in
    the environment variables.

Examples
--------
To use this module to connect to the MongoDB database:

>>> from mongo import connect
>>> client = connect()
>>> db = client.get_database("my_database")
>>> print(db.list_collection_names())

Dependencies
------------
- `dotenv` (for loading environment variables)
- `pymongo` (for MongoDB client connection)

Raises
------
SystemExit
    If this file is executed as a standalone script.
"""


import os

from dotenv import load_dotenv
from pymongo import MongoClient


def __load_env():
    """
    Load environment variables from a `.env` file.

    This function uses the `load_dotenv` function from the `dotenv` package to load
    environment variables from a file named `.env` in the current working directory.
    It is used internally by other functions in this module.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    load_dotenv()


def connect():
    """
    Establish a connection to the MongoDB database.

    This function loads the environment variables, retrieves the MongoDB connection string,
    and uses it to create a `MongoClient` instance. The connection string must be stored
    under the environment variable `MONGODB_CONNECTION_STRING` in the `.env` file.

    Parameters
    ----------
    None

    Returns
    -------
    MongoClient
        A `MongoClient` instance connected to the MongoDB database specified in the connection string.

    Raises
    ------
    Exception
        If the connection string is not found in the environment variables or if there is an error
        while establishing the connection.
    """
    __load_env()
    uri = os.getenv("MONGODB_CONNECTION_STRING")
    return MongoClient(uri)


if __name__ == '__main__':
    raise SystemExit("Cannot run this file.")
