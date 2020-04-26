"""
A Coffescript Object Notation (CSON) parser for Python 2 and Python 3.
See documentation at https://github.com/avaka/pycson
"""

from .parser import load, loads
from .writer import dump, dumps
from speg import ParseError
