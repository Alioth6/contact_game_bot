#!/usr/bin/env python

"""test.py: """

__author__      = "pavlov200912"
__maintainer__  = "Alioth6"


import sys
import os
sys.path.append(os.path.join(sys.path[0], '../src'))

import pytest
from utils import validate_file


def test_true():
    assert 2 * 2 == 4


def test_get_file_urls():
    # l = main.get_file_urls("https://en.wikipedia.org/wiki/", "Elephant")
    pass


def test_validate_file():
    assert validate_file('file-pages-articles1.xml-p1212', False)
    assert not validate_file('file-multistream-articles1.xml', False)
    assert not validate_file('file-pages-articles.xml', False)
    assert not validate_file('file-data-articles1.xml', False)


if __name__ == "__main__":
    pytest.main()
