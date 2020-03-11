#!/usr/bin/env python

"""wiki_xml_handler.py: Wiki XML handler module."""

__author__      = "pavlov200912"
__maintainer__  = "Alioth6"


import xml.sax


class WikiXmlHandler(xml.sax.handler.ContentHandler):
    """Content handler for Wiki XML data using SAX"""

    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._pages = []
        self._new_page = False
        self._page = ('', '')
        self._count_pages = 0

    def characters(self, content):
        """Characters between opening and closing tags"""
        if self._current_tag:
            self._buffer.append(content)

    def startElement(self, name, attrs):
        """Opening tag of element"""
        if name in ('title', 'text', 'timestamp'):
            self._current_tag = name
            self._buffer = []

    def endElement(self, name):
        """Closing tag of element"""
        if name == self._current_tag:
            self._values[name] = ' '.join(self._buffer)

        if name == 'page':
            self._count_pages += 1
            self._new_page = True
            self._page = (self._values['title'], self._values['text'])

    def read_page(self):
        self._new_page = False
        return self._page

    @property
    def new_page(self):
        return self._new_page
