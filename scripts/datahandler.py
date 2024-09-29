"""
Data Loading and Aggregation Utility

This module provides utility functions to retrieve and aggregate data from a MongoDB collection,
as well as to load test data or external CSV files for analysis. The primary function, `get_data`,
can operate in test mode to use predefined test data or connect to a database and CSV file
to retrieve actual data for processing.

Functions
---------
__get_test_data()
    Returns a DataFrame containing sample street data for testing purposes.
__get_test_match()
    Returns a DataFrame containing sample street data to be used for testing matching purposes.
__load_collection() -> pymongo.synchronous.collection.Collection
    Connects to the MongoDB database and retrieves the specified collection.
__aggregate_data() -> pd.DataFrame
    Aggregates data from the MongoDB collection based on a predefined aggregation pipeline.
get_data(test_flag=True, file_path=None) -> tuple[pd.DataFrame, pd.DataFrame]
    Retrieves data for analysis. If `test_flag` is True or `file_path` is not provided, it returns
    predefined test data. Otherwise, it loads data from the database and a CSV file.

Examples
--------
>>> # Using test data
>>> data, match = get_data(test_flag=True)
>>> print(data)
         STREET
0  Schloßstraße
1  Stockflethweg
2  Über den Bergen
3  Überlinger Str.
4  Goethestraße
5  Bahnhofstrasse
6  Musterstraße

>>> # Using data from MongoDB and a CSV file
>>> data, match = get_data(test_flag=False, file_path="path/to/match_file.csv")
>>> print(data.head())

Raises
------
SystemExit
    If this file is executed as a standalone script.

Notes
-----
This module relies on external configurations and environment variables for MongoDB connection settings,
as well as the aggregation pipeline definitions. Ensure that these configurations are correctly set up
before using this module.

Dependencies
------------
- `pandas`
- `pymongo`
- `config.mongo`
- `config.logger`
- `config.pipeline`
- `utils.io`

Make sure all dependencies are installed and configured correctly before using the script.
"""


import pandas as pd
import pymongo.synchronous.collection

from os import getenv, PathLike
from config.mongo import connect
from config.logger import Logger
from config.pipeline import MATCH_STAGE, PROJECTION_STAGE
from utils.io import _from_csv


def __get_test_data():
    """
    Return a sample DataFrame for testing purposes.

    This function creates and returns a sample DataFrame containing street names. It is
    used when the `get_data` function is run in test mode to simulate the format of real
    data.

    Returns
    -------
    pd.DataFrame
        A DataFrame with a single column "STREET" containing sample street names.

    Examples
    --------
    >>> __get_test_data()
            STREET
    0   Schloßstraße
    1   Stockflethweg
    2  Über den Bergen
    3  Überlinger Str.
    4   Goethestraße
    5  Bahnhofstrasse
    6   Musterstraße
    """
    return pd.DataFrame({"STREET": ["Schloßstraße", "Stockflethweg", "Über den Bergen", "Überlinger Str.",
                                    "Goethestraße", "Bahnhofstrasse", "Musterstraße"]})


def __get_test_match():
    """
    Return a sample DataFrame with street names for matching purposes.

    This function creates and returns a sample DataFrame with street names to be used
    for testing matching algorithms. It simulates the format of a real dataset that would
    be used for comparison.

    Returns
    -------
    pd.DataFrame
        A DataFrame with a single column "STREET" containing sample street names for matching.

    Examples
    --------
    >>> __get_test_match()
                     STREET
    0           Schlossstr.
    1  Ueberlinger Straße
    2      Unter der Buche
    3           Goethe Str.
    4      Stockfleterweg
    """
    return pd.DataFrame(
        {"STREET": ["Schlossstr.", "Ueberlinger Straße", "Unter der Buche", "Goethe Str.", "Stockfleterweg"]})


def __load_collection() -> pymongo.synchronous.collection.Collection:
    """
    Load the MongoDB collection based on the environment configuration.

    This function connects to the MongoDB client using credentials and settings defined in the
    environment variables. It retrieves and returns the specified collection from the database.

    Returns
    -------
    pymongo.synchronous.collection.Collection
        The MongoDB collection specified in the environment configuration.

    Raises
    ------
    KeyError
        If the environment variable `DATABASE_NAME` is not set.
    """
    client = connect()
    database = client.get_database(name=getenv("DATABASE_NAME"))
    return database.get_collection("personenMatView")


def __aggregate_data() -> pd.DataFrame:
    """
    Aggregate data from the MongoDB collection using a predefined pipeline.

    This function retrieves data from the MongoDB collection and applies an aggregation pipeline
    defined in `MATCH_STAGE` and `PROJECTION_STAGE` to filter and project the data. The results are
    then converted to a DataFrame for further processing.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the aggregated data from the MongoDB collection.
    """
    collection = __load_collection()
    return pd.DataFrame(list(__load_collection().aggregate([MATCH_STAGE, PROJECTION_STAGE])), dtype=str)


def get_data(test_flag: bool = True, file_path: PathLike[str] = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Retrieve data for analysis.

    This function can operate in two modes:
    1. **Test mode**: If `test_flag` is `True` or `file_path` is not provided, it returns predefined
       test data simulating real data.
    2. **Live mode**: If `test_flag` is `False` and a `file_path` is provided, it aggregates data from
       the MongoDB collection and loads matching data from the specified CSV file.

    Parameters
    ----------
    test_flag : bool, optional
        Flag indicating whether to use test data or live data (default is `True`).
    file_path : str or PathLike, optional
        Path to the CSV file containing matching data. If not provided, test data is used.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        A tuple containing:
        - A DataFrame with the aggregated data or test data.
        - A DataFrame with the matching data from a CSV file or test data.

    Examples
    --------
    >>> # Using test data
    >>> data, match = get_data(test_flag=True)
    >>> print(data)
             STREET
    0   Schloßstraße
    1   Stockflethweg
    2  Über den Bergen
    3  Überlinger Str.
    4   Goethestraße
    5  Bahnhofstrasse
    6   Musterstraße

    >>> # Using data from MongoDB and a CSV file
    >>> data, match = get_data(test_flag=False, file_path="path/to/match_file.csv")
    >>> print(data.head())
    """
    if test_flag or not file_path:
        return __get_test_data(), __get_test_match()
    return __aggregate_data(), _from_csv(file_path)


if __name__ == '__main__':
    log = Logger(__name__)
    log.info(f"Logger {log.get_name()} initialized.")

    df = __aggregate_data()
    log.info(df.info())
