import random
import telebot
import settings
from telebot import apihelper


bot = telebot.TeleBot(settings.TELEGRAM_API_TOKEN)


def get_random_word():
    list_words = ['cat','dog', 'brother']
    return random.choice(list_words)


def convert_question_to_word(question):
    return question.split()[0]


@bot.message_handler(commands=['start'])
def start_message(message):
    word = get_random_word()
    msg = bot.send_message(message.chat.id, 'I made a word for the letter {}.'.format(word[0]))
    bot.register_next_step_handler(msg, user_enter, word, 1)


@bot.message_handler(content_types=['text'])
def user_enter(message, word, index):
    if convert_question_to_word(message.text) == word:
        msg = bot.send_message(message.chat.id, 'Congratulations, you guessed the word {}. Run game /start'.format(word))
        return
    elif convert_question_to_word(message.text)[:index] == word[:index]:
        msg = bot.send_message(message.chat.id,'Next char: {}'.format(word[index]))
        index+=1
    else:
        msg = bot.send_message(message.chat.id, 'Try again')

    bot.register_next_step_handler(msg, user_enter, word, index)


bot.polling(none_stop=True, timeout=123)
