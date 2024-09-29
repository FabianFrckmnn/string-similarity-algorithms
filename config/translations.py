MUTATION_TRANSLATION: dict[str, str] = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}
"""
Dictionary for translating German umlaut characters to their non-diacritic equivalents.

Keys
----
str
    The umlaut charater to be replaced.
Values
------
str
    The corresponding non-diacritic replacement.
"""

ABBREVIATION_TRANSLATION: dict[str, str] = {"straße": "str.", "Straße": "Str."}


if __name__ == '__main__':
    raise SystemExit("Cannot run this file.")
