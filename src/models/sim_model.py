from collections import defaultdict

import re

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


class SimWords:
    '''
    Searching similar words for every word from sentence
    '''

    def __init__(self, a_model, a_tops=10):
        self.tops = a_tops
        self.r = re.compile("[а-яА-Я-]+")
        self.stops = stopwords.words("russian")
        self.model = a_model
        self.vocab = self.model.wv.vocab

    def is_in_vocab(self, word):
        return word in self.vocab

    def get_words(self, sentence, prefix):
        '''
        Returns a list of similar words with fixed prefix.
        List is ranged by the number of search appearance.
        '''

        # prepare the list of words from the sentence
        words = [word.lower() for word in word_tokenize(sentence) if word.isalpha()]
        words = [w for w in filter(self.r.match, words)]
        words = [word for word in words if word not in self.stops]

        # dictionary for search appears counting
        found = defaultdict(int)
        for word in words:
            if word in self.vocab:
                similar = [i[0] for i in self.model.wv.most_similar(word, topn=self.tops)]
                for elem in similar:
                    if prefix == elem[:len(prefix)]:
                        found[elem] += 1
                        
        ranged_list = sorted(found.items(), key=lambda item: item[1], reverse=True)
        res = [elem[0] for elem in ranged_list]
        
        return res
