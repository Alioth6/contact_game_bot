import sys
import os
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
from .additional_structures import Text2Lemms, WordTrie, FastText

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(PROJECT_DIR, '../data')

PATH_TO_WIGHT_FASTTEXT = os.path.join(DATA_PATH, 'ft_freqprune_400K_100K_pq_300.bin')
PATH_TO_WIKI = os.path.join(DATA_PATH, 'wiktionary_data0.csv')
DICTIONARY_SIZE = 100000

BAD_WORDS = stopwords.words("russian")
Text2LemmsModel = Text2Lemms()
FastTextModel = FastText(PATH_TO_WIGHT_FASTTEXT)


def get_wiki_words():
    df = pd.read_csv(PATH_TO_WIKI, delimiter='\\')
    text_id = df.keys()[2]
    list_defs = df[text_id]
    set_words = []
    

    for text in list_defs:
        set_words += Text2LemmsModel.get_lemms(text)

    return Counter(set_words)


def get_prefix_trie():
    stopwords.words("russian")
    words = get_wiki_words()

    for w in BAD_WORDS:
        words.pop(w, 0)

    words = [w for w,i in words.most_common(DICTIONARY_SIZE)]
    word_trie = WordTrie(FastTextModel)
    word_trie.build_dict(words)

    return word_trie
