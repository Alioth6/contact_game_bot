from collections import defaultdict

import numpy as np
from nltk.corpus import stopwords


class SimWords:
    '''
    Searching similar words for every word from sentence
    '''

    def __init__(self, a_model, a_tops=10, a_n_similar=3):
        self.tops = a_tops
        self.n_similar = a_n_similar
        self.stops = stopwords.words("russian")
        self.model = a_model

    def get_words(self, query):
        '''
        Returns a list of similar words with fixed prefix.
        List is ranged by the number of search appearance.
        '''

        words_with_prefix = query['words_with_prefix']

        # prepare the list of words from the sentence
        words = [entry['lex'] for entry in query['lem_pos_list'] if entry['lex'] not in self.stops]

        # dictionary for search appears counting
        found = defaultdict(int)
        for word in words:
            vector = self.model[word]

            def similarity(word):
                return np.dot(vector, self.model[word])

            words_with_prefix.sort(key=lambda x: similarity(x), reverse=True)
            res = words_with_prefix[:self.n_similar]
            for elem in res:
                found[elem] += 1

                        
        ranged_list = sorted(found.items(), key=lambda item: item[1], reverse=True)
        res = [elem[0] for elem in ranged_list[:self.tops]]
        
        return res
