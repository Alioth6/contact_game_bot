import telebot
from telebot import apihelper

import settings
from utils import get_random_word, convert_question_to_word


bot = telebot.TeleBot(settings.TELEGRAM_API_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    word = get_random_word()
    msg = bot.send_message(message.chat.id, 'I made a word for the letter {}.'.format(word[0]))
    bot.register_next_step_handler(msg, user_enter, word, 1)


@bot.message_handler(content_types=['text'])
def user_enter(message, word, index):
    answer = convert_question_to_word(message.text)
    if answer == word:
        msg = bot.send_message(message.chat.id, 'Congratulations, you guessed the word {}. Run game /start'.format(word))
        return
    elif answer[:index] == word[:index]:
        msg = bot.send_message(message.chat.id,'Next char: {}'.format(word[index]))
        index += 1
    else:
        msg = bot.send_message(message.chat.id, 'Try again')

    bot.register_next_step_handler(msg, user_enter, word, index)


bot.polling(none_stop=True, timeout=123)
