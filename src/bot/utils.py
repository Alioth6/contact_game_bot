import random
import shelve
from csv import writer

import src.bot.settings as conf


def set_user_data(chat_id, data):
    """
    Записываем юзера в игроки и запоминаем, что он должен ответить.
    Либо обновляем информацию.
    """
    with shelve.open(conf.USER_STATE) as storage:
        storage[str(chat_id)] = data


def set_user_state(chat_id, state):
    """
    Указываем позицию хода игрока.
    """
    with shelve.open(conf.USER_STATE) as storage:
        data = storage[str(chat_id)]
        data['state'] = state
        storage[str(chat_id)] = data


def finish_user_game(chat_id):
    """
    Заканчиваем игру текущего пользователя и удаляем правильный ответ из хранилища
    """
    with shelve.open(conf.USER_STATE) as storage:
        del storage[str(chat_id)]


def get_user_data(chat_id):
    """
    Получаем правильный ответ для текущего юзера.
    В случае, если человек просто ввёл какие-то символы, не начав игру, возвращаем None
    """
    with shelve.open(conf.USER_STATE) as storage:
        try:
            return storage[str(chat_id)]
        except KeyError:
            return None


def get_user_state(chat_id):
    with shelve.open(conf.USER_STATE) as storage:
        try:
            return storage[str(chat_id)]['state']
        except KeyError:
            return None


def get_random_word():
    return random.choice(conf.LIST_PUZZLE_NOUNS)


def convert_question_to_word(question, prefix=None):
    list_words = []
    for model in conf.LIST_MODELS:
        list_words += model.get_words(question, prefix)

    return list_words[0] if list_words else None


def add_definition(definition, word):
    # Open file in append mode
    with open(conf.DATABASE_NAME, 'a+', newline='') as db:
        csv_writer = writer(db)
        csv_writer.writerow([definition, word])


# for tests

# def convert_question_to_word(question, prefix=None):
#     return random.choice([question.split()[0], None])

