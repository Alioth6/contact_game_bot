#!/usr/bin/env python

"""data_writer.py: Writing russian dictionary dataset into csv file."""

__author__      = "pavlov200912"
__maintainer__  = "Alioth6"

import csv


class DataWriter:
    def __init__(self, file_path):
        self._file_open = False
        self._file = None
        self._writer = None
        self._path = file_path

    def _open_file(self):
        self._file_open = True
        # TODO w+?, exceptions!
        self._file = open(self._path, 'w+')
        self._writer = csv.writer(self._file, delimiter='\\')

    def write(self, data, is_wikipedia):
        try:
            title, title_data = data[0], data[1]
        except ValueError:
            return
        if not title or not title_data:
            return
        if not self._file_open:
            self._open_file()
        if is_wikipedia:
            self._writer.writerow([title, title_data])
        else:
            try:
                part_of_speech = title_data['part of speech']
                meanings = title_data['meanings']
                relations = title_data['relations']
                pharaseme = title_data['phraseme']
            except KeyError:
                return
            self._writer.writerow([title, part_of_speech, meanings, relations, pharaseme])
