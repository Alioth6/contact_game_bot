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
        '''Я загадал слово на букву {0}.
Объясни мне какое-нибудь слово на {0} так, чтобы я догадался, что это, и я открою следующую букву!'''.format(
            word[0].upper()),
        reply_markup=empty_keyboard_hider
    )
    db_utils.set_user_data(message.chat.id,
                           data={
                               'gold': word,
                               'index': 1,
                               'state': int(config.States.S_ENTER_DEFINITION)
                           })


@bot.message_handler(commands=['info'])
def info_message(message):
    msg = bot.send_message(
        message.chat.id,
        '''*Привет!*
Я бот, с которым можно играть в *контакт* :)
Механизм игры такой:

- я загадываю слово и сообщаю тебе его первую букву;

- твоя задача - объяснить мне какое-нибудь слово, начинающееся так же, так, чтобы я догадался, что это такое;

- если я угадаю, то открою тебе следующую букву.

Все загадываемые слова - существительные в неопределённой форме, имён собственных среди них нет.''',
        reply_markup=empty_keyboard_hider,
        parse_mode='Markdown'
    )


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
    send = bot.send_message(message.chat.id, "А какое слово ты загадал?")
    db_utils.set_user_state(message.chat.id, state=config.States.S_ENTER_WORD.value)


# ввод корректного слова
@bot.message_handler(
    func=lambda message: db_utils.get_user_state(message.chat.id) == config.States.S_ENTER_WORD.value,
    content_types=['text'])
def enter_word(message):
    user_data = db_utils.get_user_data(message.chat.id)
    user_data['word'] = message.text.lower().split()[0]
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
        msg = bot.send_message(message.chat.id, 'Это слово "%s"?' % word.upper(), reply_markup=markup)
        user_data['state'] = config.States.S_CHECK_WORD.value
    else:
        msg = bot.send_message(
            message.chat.id,
            "Я не знаю, что это такое. Какое слово ты загадал?"
        )
        user_data['state'] = config.States.S_ENTER_WORD.value

    db_utils.set_user_data(message.chat.id, data=user_data)


# по дефолту
@bot.message_handler(func=lambda message: True, content_types=['text'])
def default(message):
    bot.send_message(
        message.chat.id,
        """Чтобы начать игру, нажми /start ,
чтобы получить информацию об игре, нажми /info"""
    )


# проверка ответа
def check_word(message, user_data, guessed):
    word = user_data['word']
    gold = user_data['gold']
    index = user_data['index']

    db_utils.add_definition(word, user_data['definition'], guessed)

    # игрок угадал загаданное слово
    if gold == word:
        msg = bot.send_message(
            message.chat.id,
            '''Точно, это %s!
Чтобы начать игру нажми /start''' % gold.upper()
        )
        db_utils.finish_user_game(message.chat.id)
    # слово игрока начинается на верный префикс
    elif gold[:index] == word[:index]:
        if guessed:
            if len(gold) == index + 1:
                send = bot.send_message(message.chat.id,
                                        '''Ты открыл все буквы, это было слово {0}.
Чтобы начать игру нажми /start'''.format(gold.upper()))
                db_utils.finish_user_game(message.chat.id)
            else:
                send = bot.send_message(message.chat.id,
                                        '''Следующая буква - {0}.
Объясни мне что-нибудь на {1}'''.format(gold[index].upper(),
                                        gold[:index + 1].upper()))
                user_data['index'] = index + 1
        else:
            send = bot.send_message(message.chat.id, "Попробуй объяснить другое слово на %s" % gold[:index].upper())
        user_data['state'] = config.States.S_ENTER_DEFINITION.value
        db_utils.set_user_data(message.chat.id, data=user_data)
    # слово начинается на неверный префикс
    else:
        msg = bot.send_message(message.chat.id, '''Но слово должно начинаться на %s!
Попробуй объяснить мне другое слово.''' % gold[:index].upper())
        db_utils.set_user_state(message.chat.id, state=config.States.S_ENTER_DEFINITION.value)
