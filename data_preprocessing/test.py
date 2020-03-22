#!/usr/bin/env python

"""test.py: """

__author__      = "pavlov200912"
__maintainer__  = "Alioth6"


import pytest
import main


def test_true():
    assert 2 * 2 == 4


def test_get_file_urls():
    # l = main.get_file_urls("https://en.wikipedia.org/wiki/", "Elephant")
    pass


def test_validate_file():
    assert main.validate_file('file-pages-articles1.xml-p1212', False)
    assert not main.validate_file('file-multistream-articles1.xml', False)
    assert not main.validate_file('file-pages-articles.xml', False)
    assert not main.validate_file('file-data-articles1.xml', False)


if __name__ == "__main__":
    pytest.main()
