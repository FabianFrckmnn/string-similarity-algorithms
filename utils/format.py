"""
Text Normalization Utility

This module provides a utility function for normalizing text. The function `normalize_text`
applies multiple replacements to a given string, such as abbreviations and mutations, and
removes any special characters or punctuation. The resulting text is in lowercase and
stripped of leading and trailing spaces.

Attributes
----------
ABBREVIATION_TRANSLATION : dict
    A dictionary containing abbreviation replacements, loaded from `config.translations`.
MUTATION_TRANSLATION : dict
    A dictionary containing mutation replacements, loaded from `config.translations`.

Functions
---------
normalize_text(text)
    Normalizes the input text by applying abbreviation and mutation translations, and
    removes special characters and punctuation.

Raises
------
SystemExit
    If this file is executed as a standalone script.
"""


import re
from functools import reduce

from config.translations import ABBREVIATION_TRANSLATION, MUTATION_TRANSLATION


def normalize_text(text: str) -> str:
    """
    Normalize the input text using predefined replacements and character removal.

    This function applies a series of replacements to the input text based on
    dictionaries `ABBREVIATION_TRANSLATION` and `MUTATION_TRANSLATION`. It replaces
    abbreviations and mutations, removes any special characters or punctuation,
    and converts the text to lowercase.

    Parameters
    ----------
    text : str
        The input text to be normalized.

    Returns
    -------
    str
        The normalized text, with abbreviations and mutations replaced, special
        characters removed, and text converted to lowercase.

    Examples
    --------
    >>> normalize_text("Dr. Müller-Straße 123")
    'dr muellerstrasse 123'
    """
    replacements = ABBREVIATION_TRANSLATION | MUTATION_TRANSLATION
    text = reduce(lambda t, kv: re.sub(kv[0], kv[1], t), replacements.items(), text)
    return re.sub(r"[^\w\s]", "", text.lower().strip())


if __name__ == '__main__':
    raise SystemExit("Cannot run this file.")
