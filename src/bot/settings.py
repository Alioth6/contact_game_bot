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

LIST_MODELS = init_models()
