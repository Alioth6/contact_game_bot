import urllib.request
import os.path
from enum import Enum
from src.models.hyp_model import HypWords
from src.models.sim_model import SimWords
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


def init_models():
    url = 'http://panchenko.me/data/dsl-backup/w2v-ru/all.norm-sz100-w10-cb0-it1-min100.w2v'
    rdt_name = 'data/RDT_light.w2v'
    if not os.path.isfile(rdt_name):
        print('Beginning w2v file download...')
        urllib.request.urlretrieve(url, rdt_name)

    print('Loading W2v...')
    mod_rdt = KeyedVectors.load_word2vec_format(rdt_name, binary=True, unicode_errors='ignore')

    print('Models initialization...')

    # hypWords = HypWords()
    sum_words = SumWords(mod_rdt, 20)

    print('Ready')

    return [
        # hypWords,
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
