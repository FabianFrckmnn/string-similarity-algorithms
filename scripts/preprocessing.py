"""
Text Preprocessing Utility

This module provides functions for text normalization and preprocessing of data in a Pandas DataFrame.
The primary function, `preprocess`, is used to clean and normalize text data, making it suitable for
subsequent string similarity matching and comparison.

Functions
---------
__normalize_text(s1)
    Applies a series of text replacements and removes special characters from the input string.
preprocess(df, column)
    Normalizes the specified column in a DataFrame and returns the preprocessed DataFrame along with
    the normalized and original text as separate series.

Examples
--------
>>> data = pd.DataFrame({'Name': ['Dr. Müller', 'Frau Schmidt', 'Herr König']})
>>> df, normalized, original = preprocess(data, 'Name')
>>> print(normalized)
0    dr mueller
1    frau schmidt
2    herr koenig
Name: Name, dtype: object

Raises
------
SystemExit
    If this file is executed as a standalone script.
"""



import re

import pandas as pd

from functools import reduce
from config.translations import ABBREVIATION_TRANSLATION, MUTATION_TRANSLATION


def __normalize_text(s1: str) -> str:
    """
    Normalize the input text using predefined replacements and character removal.

    This function performs multiple text replacements based on dictionaries defined in
    `ABBREVIATION_TRANSLATION` and `MUTATION_TRANSLATION`. It removes special characters,
    converts the text to lowercase, and returns the cleaned string.

    Parameters
    ----------
    s1 : str
        The input string to be normalized.

    Returns
    -------
    str
        The normalized string with abbreviations replaced and special characters removed.

    Examples
    --------
    >>> __normalize_text("Dr. Müller-Straße 123")
    'dr muellerstrasse 123'
    """
    replacements = ABBREVIATION_TRANSLATION | MUTATION_TRANSLATION
    s2 = reduce(lambda s, kv: re.sub(kv[0], kv[1], s), replacements.items(), s1)
    return re.sub(r"[^\w\s]", "", s2.lower().strip())


def preprocess(df: pd.DataFrame, column: str) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """
    Preprocess a specified column in a DataFrame by normalizing the text.

    This function creates a copy of the input DataFrame, resets its index, and normalizes
    the specified column. The function returns a tuple containing the modified DataFrame,
    a Series of normalized text, and a Series of the original text.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame containing the text data to be preprocessed.
    column : str
        The name of the column in the DataFrame to be normalized.

    Returns
    -------
    tuple[pd.DataFrame, pd.Series, pd.Series]
        A tuple containing:
        - The modified DataFrame (`df_copy`) with the specified column normalized.
        - A Series of the normalized text.
        - A Series of the original text before normalization.

    Examples
    --------
    >>> data = pd.DataFrame({'Name': ['Dr. Müller', 'Frau Schmidt', 'Herr König']})
    >>> df, normalized, original = preprocess(data, 'Name')
    >>> print(normalized)
    0    dr mueller
    1    frau schmidt
    2    herr koenig
    Name: Name, dtype: object
    """
    df_copy = df.copy()
    df_copy = df_copy.reset_index(drop=True, inplace=False)
    df_copy[column] = df_copy[column].fillna("", inplace=False)

    normalized_series = df_copy[column].apply(__normalize_text)
    original_series = df_copy[column]
    return df_copy, normalized_series, original_series


if __name__ == '__main__':
    raise SystemExit("Cannot run this file.")
