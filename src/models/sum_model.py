import re

import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class SumWords:
    '''
    Searching similar words for sentence words sum
    '''

    def __init__(self, a_model, a_trie, a_tops=10):
        self.model = a_model
        self.prefix_trie = a_trie
        self.tops = a_tops
        self.r = re.compile("[а-яА-Я-]+")
        self.stops = stopwords.words("russian")
        self.vocab = self.model.wv.vocab


    def is_in_vocab(self, word):
        return word in self.vocab

    def get_words(self, sentence, prefix):
        '''
        Returns a list of similar words with fixed prefix.
        List is ranged by similarity level.
        '''

        words_with_prefix = list(w[0] for w in self.prefix_trie.search_by_prefix(prefix))

        # prepare the list of words from the sentence
        words = [word.lower() for word in word_tokenize(sentence) if word.isalpha()]
        words = [w for w in filter(self.r.match, words)]
        words = [word for word in words if word not in self.stops]

        # we are using fasttext - so we don't check if a word is in the dictionary
        if words:
            sum_vector = sum([self.model[word] for word in words])

            def similarity(word):
                return np.dot(sum_vector, self.model[word])

            words_with_prefix.sort(key=lambda x: similarity(x), reverse=True)

            res = words_with_prefix[:self.tops]
        else:
            return []

        return res
