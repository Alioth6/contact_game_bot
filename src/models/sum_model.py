import numpy as np
from nltk.corpus import stopwords


class SumWords:
    '''
    Searching similar words for sentence words sum
    '''

    def __init__(self, a_model, a_tops=10):
        self.model = a_model
        self.tops = a_tops
        self.stops = stopwords.words("russian")

    def get_words(self, query):
        '''
        Returns a list of similar words with fixed prefix.
        List is ranged by similarity level.
        '''
        words_with_prefix = query['words_with_prefix']

        # prepare the list of words from the sentence
        words = [entry['lex'] for entry in query['lem_pos_list'] if entry['lex'] not in self.stops]

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
