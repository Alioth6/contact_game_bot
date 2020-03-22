import random


def get_random_word():
    list_words = ['cat','dog', 'brother']
    return random.choice(list_words)


def convert_question_to_word(question):
    return question.split()[0]
