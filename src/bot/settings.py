from enum import Enum
from src.models.hyp_model import HypWords
from src.models.sim_model import SimWords


TELEGRAM_API_TOKEN = 'token'

USER_STATE = 'data/user_state'  # Файл с хранилищем
DATABASE_NAME = 'data/definition.db'  # Файл с базой данных


class States(Enum):
    S_ENTER_DEFINITION = 0
    S_ENTER_WORD = 1
    S_CHECK_WORD = 2


def init_models():
    # SimWords(, a_tops=1) - хз как загружать
    hypWords = HypWords()
    return [
        hypWords
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
