import logging

import telebot
from telebot import types

import src.bot.settings as config
from config import Config

bot = telebot.TeleBot(Config.TOKEN)
empty_keyboard_hider = types.ReplyKeyboardRemove()

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

from src.bot import utils as db_utils


exceptions = []


@bot.message_handler(commands=['start'])
def start_message(message):
    word = config.get_random_word().upper()
    bot.send_message(
        message.chat.id,
        'Я загадал слово на букву %s.' % word[0],
        reply_markup=empty_keyboard_hider
    )
    db_utils.set_user_data(message.chat.id,
                           data={
                               'gold': word.lower(),
                               'index': 1,
                               'state': int(config.States.S_ENTER_DEFINITION)
                           })
    exceptions.clear()


# модель угадала слово
@bot.message_handler(
    func=lambda message: db_utils.get_user_state(message.chat.id) == config.States.S_CHECK_WORD.value \
                         and message.text == 'Да',
    content_types=['text'])
def enter_yes(message):
    user_data = db_utils.get_user_data(message.chat.id)
    check_word(message, user_data, guessed=True)


# модель не угадала слово
@bot.message_handler(
    func=lambda message: db_utils.get_user_state(message.chat.id) == config.States.S_CHECK_WORD.value \
                         and message.text == 'Нет',
    content_types=['text'])
def enter_no(message):
    bot.send_message(message.chat.id, "Я не смог угадать слово. Введи загаданное слово.")
    db_utils.set_user_state(message.chat.id, state=config.States.S_ENTER_WORD.value)


# ввод корректного слова
@bot.message_handler(
    func=lambda message: db_utils.get_user_state(message.chat.id) == config.States.S_ENTER_WORD.value,
    content_types=['text'])
def enter_word(message):
    user_data = db_utils.get_user_data(message.chat.id)
    user_data['word'] = message.text
    check_word(message, user_data, guessed=False)


# ввод определения
@bot.message_handler(
    func=lambda message: db_utils.get_user_state(message.chat.id) == config.States.S_ENTER_DEFINITION.value,
    content_types=['text'])
def enter_definition(message):
    user_data = db_utils.get_user_data(message.chat.id)
    definition = message.text
    gold = user_data['gold']
    index = user_data['index']

    word = config.convert_question_to_word(definition, gold[:index])
    user_data['definition'] = definition
    user_data['word'] = word

    if word:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Да', 'Нет')  # Имена кнопок
        bot.send_message(message.chat.id, 'Это слово "%s"?' % word, reply_markup=markup)
        user_data['state'] = config.States.S_CHECK_WORD.value
    else:
        bot.send_message(
            message.chat.id,
            "Я не знаю этого слова. Введи загаданное слово."
        )
        user_data['state'] = config.States.S_ENTER_WORD.value

    db_utils.set_user_data(message.chat.id, data=user_data)


# по дефолту
@bot.message_handler(func=lambda message: True, content_types=['text'])
def default(message):
    bot.send_message(
        message.chat.id,
        """Чтобы начать игру, нажмите /start, чтобы получить информацию об игре, нажмите /info"""
    )


# проверка ответа
def check_word(message, user_data, guessed):
    word = user_data['word']
    gold = user_data['gold']
    index = user_data['index']

    if word not in exceptions:
        db_utils.add_definition(word, user_data['definition'], guessed)

    if gold.lower() == word.lower():
        bot.send_message(
            message.chat.id,
            'Поздравляем, ты угадал слово! Чтобы начать игру нажми /start'
        )
        db_utils.finish_user_game(message.chat.id)
    elif gold.lower()[:index] == word.lower()[:index]:
        if word in exceptions:
            bot.send_message(message.chat.id,
                             "Ты уже называл это слово! Введи что-нибудь новенькое, пожалуйста:)")
            user_data['state'] = config.States.S_ENTER_DEFINITION.value
            db_utils.set_user_data(message.chat.id, data=user_data)
        elif index < len(gold):
            bot.send_message(message.chat.id, "Следующая буква: %s" % gold.upper()[index])
            user_data['index'] = index + 1
            exceptions.append(word)
            user_data['state'] = config.States.S_ENTER_DEFINITION.value
            db_utils.set_user_data(message.chat.id, data=user_data)
        else:
            bot.send_message(message.chat.id,
                             "Это победа, поздравляем! Ты дошёл до конца загаданного слова:) Чтобы начать игру нажми "
                             "/start")
            db_utils.finish_user_game(message.chat.id)
    else:
        if word not in exceptions:
            exceptions.append(word)
            bot.send_message(message.chat.id,
                             '''Слово должно начинаться на %s. Попробуйте ввести определение слова сначала'''
                             % gold.upper()[:index])
        db_utils.set_user_state(message.chat.id, state=config.States.S_ENTER_DEFINITION.value)
