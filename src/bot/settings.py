import random
from enum import IntEnum

import compress_fasttext
import smart_open

from config import Config
from src.models.hyp_model import HypWords
# from src.models.sim_model import SimWords
from src.models.sum_model import SumWords
from src.utils.additional_structures import WordTrie
# from src.utils.spell_checker import Spell_checker
from src.utils.text_to_lemms import Text2Lemms

LIST_MODELS = []
NORMALIZER = None
NOUNS_TRIE = None


class States(IntEnum):
    S_ENTER_DEFINITION = 0
    S_ENTER_WORD = 1
    S_CHECK_WORD = 2


def init_puzzle_nouns():
    nouns_list_name = ''.join([
        Config.DATA_PATH,
        Config.NOUNS_FILE_NAME
    ])

    with smart_open.open(nouns_list_name) as f:
        puzzle_nouns = [string.strip() for string in f]

    return puzzle_nouns


LIST_PUZZLE_NOUNS = init_puzzle_nouns()


def init_converter():
    print('Models initialization...')

    fasttext_mod_path = ''.join([
        Config.DATA_PATH,
        Config.MODEL_FILE_NAME
    ])

    fasttext_mod = compress_fasttext.models.CompressedFastTextKeyedVectors.load(fasttext_mod_path)

    global NOUNS_TRIE
    NOUNS_TRIE = WordTrie(fasttext_mod)
    global LIST_PUZZLE_NOUNS
    NOUNS_TRIE.build_dict(LIST_PUZZLE_NOUNS)

    hyp_words = HypWords(1)
    sum_words = SumWords(fasttext_mod, 1)

    global LIST_MODELS
    LIST_MODELS = [
        hyp_words,
        sum_words
    ]

    print('Normalizer initialization...')

    dict_file_name = ''.join([
        Config.DATA_PATH,
        Config.DICT_FILE_NAME
    ])

    # reading dictionary file to list
    # with smart_open.open(dict_file_name) as f:
    #     words_list = [string.strip() for string in f]

    # build all dictionary based word trie
    # words_trie = WordTrie(fasttext_mod)
    # words_trie.build_dict(words_list)

    # spell_checker = Spell_checker(words_trie)
    global NORMALIZER
    # NORMALIZER = Text2Lemms(spell_checker)
    NORMALIZER = Text2Lemms()

    print('Ready')


def get_random_word():
    return random.choice(LIST_PUZZLE_NOUNS)


def convert_question_to_word(question, prefix=None):
    # the list of lemmatized and checked words with PoS tags
    lem_pos_list = NORMALIZER.get_lemms(question)
    words_with_prefix = list(w[0] for w in NOUNS_TRIE.search_by_prefix(prefix))

    query = {
        'sentence': question,
        'prefix': prefix,
        'lem_pos_list': lem_pos_list,
        'words_with_prefix': words_with_prefix
    }

    # classifier returns the list of indices of models to process
    indices = list(range(len(LIST_MODELS)))

    pos_string = NORMALIZER.get_pos_string()
    if pos_string.count('s') > 1 or pos_string.count('g') > 0:
        indices = [1]

    list_words = []
    for i in indices:
        list_words += LIST_MODELS[i].get_words(query)
        if list_words:
            break

    return list_words[0] if list_words else None
