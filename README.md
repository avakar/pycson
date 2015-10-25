[![Build Status](https://travis-ci.org/avakar/pycson.svg?branch=master)](https://travis-ci.org/avakar/pycson)

# pycson

This is a python parser for the Coffeescript Object Notation (CSON).

Install:

    pip install pycson

The interface is the same as for the standard `json` package.

    >>> import cson
    >>> cson.loads('a: 1')
    {'a': 1}
    >>> with open('file.cson', 'rb') as fin:
    ...     obj = cson.load(fin)
    >>> obj
    {'a': 1}
