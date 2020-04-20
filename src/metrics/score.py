from src.utils.dictionary import fastTextModel as fasttext
from src.utils.dictionary import get_prefix_trie


DISTANSE_MIN = 0.55


class NaiveMetric():
    def __init__(self):
        self.n_success = 0
        self.n_test = 0

    def update(self, word, ordered_words, prefix=None):
        self.n_test += 1
        if word in ordered_words:
            self.n_success += 1

    def score(self):
        return self.n_success / self.n_test


class TopWords(NaiveMetric):
    def __init__(self, prefix_trie=None):
        super().__init__()
        self.prefix_trie = prefix_trie if prefix_trie else get_prefix_trie()

    def update(self, word, ordered_words, prefix):
        self.n_test += 1
        top_w = get_top_words_with_prefix(word, prefix, self.prefix_trie)

        if set(top_w) & set(ordered_words):
            self.n_success += 1


class TopRangeWords(TopWords):
    def __init__(self, prefix_trie=None):
        super().__init__(prefix_trie)
        self.num_top = 10
        self.eps = 1 / self.num_top

    def update(self, word, ordered_words, prefix):
        self.n_test += 1

        top_w = get_top_words_with_prefix(word, prefix, self.prefix_trie)
        top_w = [ k for k, v in sorted(top_w.items(), 
                    key=lambda item: -item[1])][:self.num_top]
        for i, w in enumerate(top_w):
            if w in ordered_words:
                self.n_success += 1-i*self.eps
                return


def get_top_words_with_prefix(word_gold, prefix, prefix_trie):
    dict_similarity = {}
    ans = [i[0] for i in prefix_trie.search_by_prefix(prefix)]
    if word_gold not in ans:
        prefix_trie.add(word_gold)
        ans.append(word_gold)

    for word in ans:
        dist = fasttext.model.similarity(word_gold, word)
        if dist > DISTANSE_MIN:
            dict_similarity[word] = dist
    return dict_similarity
