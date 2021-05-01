import random
from enum import IntEnum

import compress_fasttext
import smart_open

from config import Config
# from src.models.hyp_model import HypWords
# from src.models.sim_model import SimWords
from src.models.sum_model import SumWords

LIST_MODELS = []


class States(IntEnum):
    S_ENTER_DEFINITION = 0
    S_ENTER_WORD = 1
    S_CHECK_WORD = 2


def init_puzzle_nouns():
    nouns_list_name = ''.join([
        Config.DATA_PATH,
        Config.NOUNS_FILE_NAME
    ])

    puzzle_nouns = []

    with smart_open.open(nouns_list_name) as f:
        puzzle_nouns = [string.strip() for string in f]

    return puzzle_nouns


LIST_PUZZLE_NOUNS = init_puzzle_nouns()


def init_models():
    print('Models initialization...')

    fasttext_mod_path = ''.join([
        Config.DATA_PATH,
        Config.MODEL_FILE_NAME
    ])

    fasttext_mod = compress_fasttext.models.CompressedFastTextKeyedVectors.load(fasttext_mod_path)

    sum_words = SumWords(fasttext_mod, 20)

    print('Ready')

    global LIST_MODELS
    LIST_MODELS = [
        sum_words
    ]


def get_random_word():
    return random.choice(LIST_PUZZLE_NOUNS)


def convert_question_to_word(question, prefix=None):
    list_words = []
    for model in LIST_MODELS:
        list_words += model.get_words(question, prefix)

    return list_words[0] if list_words else None
