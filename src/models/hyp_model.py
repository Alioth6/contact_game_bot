from wiki_ru_wordnet import WikiWordnet

from src.utils.features_sentence import search_simple_bigramm
from src.utils.dictionary import text2LemmsModel, get_prefix_trie


class HypWords:
    # hyponym and hypernym words
    def __init__(self, prefix_trie=None):
        self.wikiwordnet = WikiWordnet()
        self.prefix_trie = get_prefix_trie() # перенести потом в бота, инициализировать перед запуском, как и остальные модели

    def _get_hyp_with_prefix(self, word, words_with_prefix):
        hyp_w = get_hyponym_and_hypernym(self.wikiwordnet, word)
        answer = hyp_w & words_with_prefix
        if answer:
            return list(answer)
        return []

    def is_in_vocab(self, word):
        return True

    def get_words(self, sentence, prefix):
        list_lex = text2LemmsModel.get_lemms(sentence)
        bigramm_w = search_simple_bigramm(list_lex)
        words_with_prefix = set(w[0] for w in self.prefix_trie.search_by_prefix(prefix))
        word = None

        if bigramm_w:
            bigramm = ' '.join(bigramm_w)
            ans = self._get_hyp_with_prefix(bigramm, words_with_prefix)
            if ans:
                return ans
            word = bigramm_w[1]
        else:
            for w in list_lex:
                if w['pos'] == 'S':
                    word = w['lex']
                    break

        return self._get_hyp_with_prefix(word, words_with_prefix)


def get_hyponym_and_hypernym(wikiwordnet, word):
    synsets = wikiwordnet.get_synsets(word)
    set_words = set()

    if not synsets:
        return set_words

    synset1 = synsets[0]

    for hyponym in wikiwordnet.get_hyponyms(synset1):
        set_words |= { w.lemma() for w in hyponym.get_words()}

    for hypernym in wikiwordnet.get_hypernyms(synset1):
        set_words |= { w.lemma() for w in hypernym.get_words()}

    return set_words
