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


@bot.message_handler(commands=['start'])
def start_message(message):
    word = config.get_random_word()
    msg = bot.send_message(
        message.chat.id,
        'Я загадал слово на букву %s.' % word[0],
        reply_markup=empty_keyboard_hider
    )
    db_utils.set_user_data(message.chat.id,
                           data={
                               'gold': word,
                               'index': 1,
                               'state': int(config.States.S_ENTER_DEFINITION)
                           })


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
    send = bot.send_message(message.chat.id, "Я не смог угадать слово. Введи загаданное слово.")
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
        msg = bot.send_message(message.chat.id, 'Это слово "%s"?' % word, reply_markup=markup)
        user_data['state'] = config.States.S_CHECK_WORD.value
    else:
        msg = bot.send_message(
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
        """Чтобы начать игру, нажмите /start ,
чтобы получить информацию об игре, нажмите /info"""
    )


# проверка ответа
def check_word(message, user_data, guessed):
    word = user_data['word']
    gold = user_data['gold']
    index = user_data['index']

    db_utils.add_definition(word, user_data['definition'], guessed)

    if gold == word:
        msg = bot.send_message(
            message.chat.id,
            'Поздравляем, ты угадал слово! Чтобы начать игру нажми /start'
        )
        db_utils.finish_user_game(message.chat.id)
    elif gold[:index] == word[:index]:
        send = bot.send_message(message.chat.id, "Следующая буква: %s" % gold[index])
        user_data['index'] = index + 1
        user_data['state'] = config.States.S_ENTER_DEFINITION.value
        db_utils.set_user_data(message.chat.id, data=user_data)
    else:
        msg = bot.send_message(message.chat.id, '''Слово должно начинаться на %s.
Попробуйте ввести определение слова сначала''' % gold[:index])
        db_utils.set_user_state(message.chat.id, state=config.States.S_ENTER_DEFINITION.value)
