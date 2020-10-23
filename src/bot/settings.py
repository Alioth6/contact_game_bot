import urllib.request
import os.path
import compress_fasttext
from enum import Enum
# from src.models.hyp_model import HypWords
# from src.models.sim_model import SimWords
from src.models.sum_model import SumWords
from gensim.models import KeyedVectors
from gensim.models.word2vec import Word2Vec

TELEGRAM_API_TOKEN = '1079775223:AAHzut5iNPZZIzPLbIOFL0NaVXnleTdTy0A'

USER_STATE = 'data/user_state'  # Файл с хранилищем
DATABASE_NAME = 'data/database.csv'  # Файл с базой данных


class States(Enum):
    S_ENTER_DEFINITION = 0
    S_ENTER_WORD = 1
    S_CHECK_WORD = 2


def init_no_models():
    print('Ready')

    return []


def init_models():
    print('Models initialization...')

    fasttext_mod_path = 'http://s3.amazonaws.com/contact-game-model/ft_freqprune_400K_100K_pq_300.bin'
    fasttext_mod = compress_fasttext.models.CompressedFastTextKeyedVectors.load(fasttext_mod_path)

    sum_words = SumWords(fasttext_mod, 20)

    print('Ready')

    return [
        sum_words
    ]


def init_puzzle_nouns():
    nouns_list_name = 'data/freq_nouns.txt'

    puzzle_nouns = []

    with open(nouns_list_name) as f:
        for i in f:
            puzzle_nouns.append(i[:-1])

    return puzzle_nouns


LIST_MODELS = init_models()
LIST_PUZZLE_NOUNS = init_puzzle_nouns()
