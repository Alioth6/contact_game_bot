import compress_fasttext
import smart_open
from enum import Enum
from config import Config
import os
# from src.models.hyp_model import HypWords
# from src.models.sim_model import SimWords
from src.models.sum_model import SumWords


USER_STATE = 'data/user_state'  # Файл с хранилищем
DATABASE_NAME = 'data/database.csv'  # Файл с базой данных

LIST_MODELS = []


class States(Enum):
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
