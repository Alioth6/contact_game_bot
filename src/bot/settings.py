import compress_fasttext
from enum import Enum
import os
# from src.models.hyp_model import HypWords
# from src.models.sim_model import SimWords
from src.models.sum_model import SumWords


TELEGRAM_API_TOKEN = os.environ['TOKEN']

S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

USER_STATE = 'data/user_state'  # Файл с хранилищем
DATABASE_NAME = 'data/database.csv'  # Файл с базой данных

LIST_MODELS = []


class States(Enum):
    S_ENTER_DEFINITION = 0
    S_ENTER_WORD = 1
    S_CHECK_WORD = 2


def init_no_models():
    print('Ready')

    return []


def init_models():
    print('Models initialization...')

    model_file_name = 'ft_freqprune_100K_20K_pq_300.bin'
    fasttext_mod_url = ''.join([
        's3://',
        AWS_ACCESS_KEY_ID,
        ":",
        AWS_SECRET_ACCESS_KEY,
        '@',
        S3_BUCKET_NAME,
        '/',
        model_file_name
    ])

    fasttext_mod = compress_fasttext.models.CompressedFastTextKeyedVectors.load(fasttext_mod_url)

    sum_words = SumWords(fasttext_mod, 20)

    print('Ready')

    return [
        sum_words
    ]


def fill_list_models():
    global LIST_MODELS
    LIST_MODELS = init_models()


def init_puzzle_nouns():
    nouns_list_name = 'data/freq_nouns.txt'

    puzzle_nouns = []

    with open(nouns_list_name) as f:
        puzzle_nouns = [string.strip() for string in f]

    return puzzle_nouns


LIST_PUZZLE_NOUNS = init_puzzle_nouns()
