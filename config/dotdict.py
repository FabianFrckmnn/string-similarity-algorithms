"""
DotDict: A dictionary subclass that allows dot notation access to dictionary attributes.

This class extends the built-in Python `dict` to provide attribute-style access to its keys.
It allows users to access, set, and delete dictionary items using dot notation in addition
to the standard bracket notation.

Examples
--------
>>> d = DotDict({'key1': 'value1', 'key2': 'value2'})
>>> print(d.key1)         # Access using dot notation
'value1'
>>> d.key3 = 'value3'     # Set new key-value pair using dot notation
>>> print(d['key3'])      # Access using bracket notation
'value3'
>>> del d.key1            # Delete key using dot notation
>>> print(d.get('key1'))  # Access using get method
None

Attributes
----------
None

Methods
-------
__getattr__(name)
    Retrieves the value associated with `name` if it exists, otherwise raises AttributeError.
__setattr__(name, value)
    Sets the key `name` to the specified `value`.
__delattr__(name)
    Deletes the key `name` from the dictionary.

Raises
------
AttributeError
    If attempting to access a non-existent attribute.
"""


class DotDict(dict):
    """
    A dictionary subclass that supports attribute-style access.

    This class overrides the built-in `dict` methods to enable dot notation for getting,
    setting, and deleting items. It provides a more flexible interface for accessing
    dictionary data.

    Methods
    -------
    __getattr__(name)
        Retrieves the value associated with `name` if it exists, otherwise raises AttributeError.
    __setattr__(name, value)
        Sets the key `name` to the specified `value`.
    __delattr__(name)
        Deletes the key `name` from the dictionary.
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


if __name__ == '__main__':
    raise SystemExit("Cannot run this file.")
