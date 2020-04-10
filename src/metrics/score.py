from src.utils.dictionary import fastTextModel as fasttext
from src.utils.dictionary import get_prefix_trie


DISTANSE_MIN = 0.55
prefix_trie = get_prefix_trie()


class Naive_metric():
    def __init__(self):
        self.n_success = 0
        self.n_test = 0

    def update(self, word, ordered_words, prefix=None):
        self.n_test += 1
        if word in ordered_words:
            self.n_success += 1

    def score(self):
        return self.n_success / self.n_test


class TopWords(Naive_metric):
    def update(self, word, ordered_words, prefix):
        self.n_test += 1
        top_w = get_top_words_with_prefix(word, prefix)

        if set(top_w) & set(ordered_words):
            self.n_success += 1


class TopRangeWords(Naive_metric):
    def __init__(self):
        super().__init__()
        self.num_top = 10
        self.eps = 1 / self.num_top

    def update(self, word, ordered_words, prefix):
        self.n_test += 1

        top_w = get_top_words_with_prefix(word, prefix)
        top_w = [ k for k, v in sorted(top_w.items(), 
                    key=lambda item: -item[1])][:self.num_top]
        for i, w in enumerate(top_w):
            if w in ordered_words:
                self.n_success += 1-i*self.eps
                return


def get_top_words_with_prefix(word_gold, prefix):
    dict_similarity = {}
    ans = [i[0] for i in prefix_trie.search_by_prefix(prefix)]

    for word in ans:
        dist = fasttext.model.similarity(word_gold, word)
        if dist > DISTANSE_MIN:
            dict_similarity[word] = dist
    return dict_similarity
