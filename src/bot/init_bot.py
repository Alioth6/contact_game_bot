from flask import Flask, request

import logging

import src.bot.settings as config
from src.bot import utils

import telebot
from telebot import types


bot = telebot.TeleBot(config.TELEGRAM_API_TOKEN)
empty_keyboard_hider = types.ReplyKeyboardRemove()

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start_message(message):
    word = utils.get_random_word()
    msg = bot.send_message(
        message.chat.id, 
        'Я загадал слово на букву %s.' % word[0], 
        reply_markup=empty_keyboard_hider
    )
    utils.set_user_data(message.chat.id,
    data={
        'gold': word, 
        'index': 1,
        'state': config.States.S_ENTER_DEFINITION.value
    })


# модель угадала слово
@bot.message_handler(
    func=lambda message: utils.get_user_state(message.chat.id)==config.States.S_CHECK_WORD.value \
    and message.text=='Да',
    content_types=['text'])
def enter_yes(message):
    user_data = utils.get_user_data(message.chat.id)
    check_word(message, user_data)


# модель не угадала слово
@bot.message_handler(
    func=lambda message: utils.get_user_state(message.chat.id)==config.States.S_CHECK_WORD.value\
    and message.text=='Нет',
    content_types=['text'])
def enter_no(message):
    send = bot.send_message(message.chat.id, "Я не смог угадать слово. Введи загаданное слово." )
    utils.set_user_state(message.chat.id, state=config.States.S_ENTER_WORD.value)


# ввод корректного слова
@bot.message_handler(
    func=lambda message: utils.get_user_state(message.chat.id)==config.States.S_ENTER_WORD.value, 
    content_types=['text'])
def enter_word(message):
    user_data = utils.get_user_data(message.chat.id)
    user_data.update({
        'word': message.text
    })
    check_word(message, user_data)


# ввод определения
@bot.message_handler(
    func=lambda message: utils.get_user_state(message.chat.id)==config.States.S_ENTER_DEFINITION.value,
    content_types=['text'])
def enter_definition(message):
    user_data = utils.get_user_data(message.chat.id)
    definition = message.text
    gold = user_data['gold']
    index = user_data['index']
    
    word = utils.convert_question_to_word(definition, gold[:index])
    user_data.update({
        'definition': definition,
        'word': word
    })

    if word:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Да', 'Нет') # Имена кнопок
        msg = bot.send_message(message.chat.id, 'Это слово "%s"?'% word, reply_markup=markup)
        user_data['state'] = config.States.S_CHECK_WORD.value
    else:
        msg = bot.send_message(
            message.chat.id, 
            "Я не знаю этого слова. Введи загаданное слово."
        )
        user_data['state'] = config.States.S_ENTER_WORD.value
    utils.set_user_data(message.chat.id, data=user_data)


# по дефолту
@bot.message_handler(func=lambda message: True, content_types=['text'])
def default(message):
    bot.send_message(
        message.chat.id, 
        """Чтобы начать игру, нажмите /start ,
чтобы получить информацию об игре, нажмите /info"""
    )

@server.route('/' + config.TELEGRAM_API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    print('Removing previous webhook')
    bot.remove_webhook()
    webhook_url = 'https://intense-cove-71886.herokuapp.com/' + config.TELEGRAM_API_TOKEN
    print('New webhook:')
    print(webhook_url)
    bot.set_webhook(url=webhook_url)
    return "!", 200

# проверка ответа
def check_word(message, user_data):
    word = user_data['word']
    gold = user_data['gold']
    index = user_data['index']

    utils.add_definition(user_data['definition'], word)

    if gold == word:
        msg = bot.send_message(
            message.chat.id, 
            'Поздравляем, ты угадал слово! Чтобы начать игру нажми /start'
        )
        utils.finish_user_game(message.chat.id)
    elif gold[:index] == word[:index]:
        send = bot.send_message(message.chat.id, "Следующая буква: %s" % gold[index])
        user_data.update({
            'index': index+1,
            'state': config.States.S_ENTER_DEFINITION.value
        })
        utils.set_user_data(message.chat.id, data=user_data)
    else:
        msg = bot.send_message(message.chat.id, '''Слово должно начинаться на %s.
Попробуйте ввести определение слова сначала''' % gold[:index])
        utils.set_user_state(message.chat.id, state=config.States.S_ENTER_DEFINITION.value)
