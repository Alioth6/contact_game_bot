#!/usr/bin/env python

"""main.py: Main file of russian dictionary dataset generation."""

__author__      = "pavlov200912"
__maintainer__  = "Alioth6"

import xml
import os
import requests
import subprocess
import re
import tensorflow
import multiprocessing as mp

from bs4 import BeautifulSoup
from keras.utils import get_file

from src.data_preprocessing.wiki_xml_handler import WikiXmlHandler
from src.data_preprocessing.wiki_code_parser import WikiCodeParser
from src.data_preprocessing.data_writer import DataWriter
from src.utils import validate_file

# List of lists to single list
from itertools import chain

# Sending keyword arguments in map
from functools import partial


def bytes_to_unicode(bytes):
    return bytes.decode('utf8').replace(u'\xa0', u' ')


def get_file_urls(base_url, version, download_full=False):
    """Parse file urls from wiki dump page"""
    print('get_file_urls', base_url, version, download_full)
    
    dump_url = base_url + version

    dump_html = requests.get(dump_url).text

    soup_dump = BeautifulSoup(dump_html, 'html.parser')

    files = []
    for file in soup_dump.find_all('li', {'class': 'file'}):
        text = file.text
        if validate_file(text, download_full):
            files.append(text.split()[0])
    return files


def download_files(files, target_dir, url):
    """Download files by URLS, function get_file use TensorFlow"""
    print('download_files', files, target_dir, url)
    data_paths = []
    for file in files:
        path = target_dir + file
        data_path = get_file(file, url + file) if not os.path.exists(path) else path
        data_paths.append(path)
    print('All files downloaded')
    return data_paths


def parse_dumped_file(input_file, output_file, is_wikipedia):
    handler = WikiXmlHandler()
    xml_parser = xml.sax.make_parser()
    xml_parser.setContentHandler(handler)
    writer = DataWriter(output_file)
    wiki_parser = WikiCodeParser(is_wikipedia)
    # bzcat = console utility, read .bz compressed file line by line
    count = 0
    for i, line in enumerate(subprocess.Popen(['bzcat'],
                                              stdin=open(input_file),
                                              stdout=subprocess.PIPE).stdout):
        # Parse XML file line by line, return data to handler data[0] - page title, data[1] - page data
        xml_parser.feed(bytes_to_unicode(line))

        # If handler gets signal, that xml_parser read new page:
        if handler.new_page:
            count += 1
            if count % 1000 == 0:
                print('{0} th pages processed'.format(count // 1000))
            # 1) Get this data
            data = handler.read_page()
            try:
                # 2) Load it to parser of wiki code
                wiki_parser.feed(data[0], data[1])
            except IndexError:
                continue
            # 3) Get data from wiki code parser
            data = wiki_parser.get_data()
            wiki_parser.clear()
            # 4) Write it to csv file
            writer.write(data, is_wikipedia)


if __name__ == '__main__':
    print("Do you want to download wikipedia-(1) or wiktionary-(2)? (1/2)")
    state = int(input())
    WIKI = 1

    url_tail = 'ruwiki' if state == WIKI else 'ruwiktionary'
    base_url = 'https://dumps.wikimedia.org/{0}/'.format(url_tail)
    download_full = state != WIKI
    is_wiki = state == WIKI
    file_csv_name = 'wikipedia_data' if state == WIKI else 'wiktionary_data'

    # TODO get the newer dump automatically
    version = '20200301/'
    # recommended keras path: '/home/sp/.keras/datasets/'
    # WARNING: LINUX OS PATH
    keras_home = input("Input directory path, where you want to store dumped wiki-files\n")
    file_urls = get_file_urls(base_url, version, download_full=download_full)
    file_paths = download_files(file_urls, keras_home, base_url + version)

    # Creating processes, number is corresponding to kernels count
    pool = mp.Pool(processes=mp.cpu_count())
    task_args = [(file, file_csv_name + str(i) + '.csv', is_wiki) for i, file in enumerate(file_paths)]
    # Every process will run parse_dumped_file function
    results = pool.starmap(parse_dumped_file, task_args)

    pool.close()
    pool.join()
