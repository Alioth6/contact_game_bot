import re

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


class SumWords:
    '''
    Searching similar words for sentence words sum
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
        List is ranged by similarity level.
        '''

        # prepare the list of words from the sentence
        words = [word.lower() for word in word_tokenize(sentence) if word.isalpha()]
        words = [w for w in filter(self.r.match, words)]
        words = [word for word in words if word not in self.stops]

        words = [word for word in words if word in self.vocab]
        if words != []:
            sum_similar = self.model.wv.most_similar(positive=words, topn=self.tops)
            res = [i[0] for i in sum_similar if prefix == i[0][:len(prefix)]]
        else:
            return []
        
        return res
