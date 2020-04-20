from wiki_ru_wordnet import WikiWordnet

from src.utils.features_sentence import search_simple_bigramm
from src.utils.dictionary import text2LemmsModel, get_prefix_trie


def get_hyponym_and_hypernym(wikiwordnet, word):
    synsets = wikiwordnet.get_synsets(word)
    if not synsets:
        return {}

    synset1 = synsets[0]
    set_words = set()

    for hyponym in wikiwordnet.get_hyponyms(synset1):
        set_words |= { w.lemma() for w in hyponym.get_words()}

    for hypernym in wikiwordnet.get_hypernyms(synset1):
        set_words |= { w.lemma() for w in hypernym.get_words()}

    return set_words


class HypWords:
    # hyponym and hypernym words
    def __init__(self, prefix_trie=None):
        self.wikiwordnet = WikiWordnet()
        self.prefix_trie = get_prefix_trie() # перенести потом в бота, инициализировать перед запуском, как и остальные модели

    def get_hyp_with_prefix(self, word, words_with_prefix):
        hyp_w = get_hyponym_and_hypernym(self.wikiwordnet, word)
        answer = hyp_w & words_with_prefix
        if answer:
            return list(answer)

    def get_words(self, sentence, prefix):
        list_lex = text2LemmsModel.get_lemms(sentence)
        bigramm_w = search_simple_bigramm(list_lex)
        words_with_prefix = set(w[0] for w in self.prefix_trie.search_by_prefix(prefix))
        word = None

        if bigramm_w:
            bigramm = ' '.join(bigramm_w)
            ans = self.get_hyp_with_prefix(bigramm, words_with_prefix)
            if ans:
                return ans
            word = bigramm_w[1]
        else:
            for w in list_lex:
                if w['pos'] == 'S':
                    word = w['lex']
                    break

        return self.get_hyp_with_prefix(word, words_with_prefix)
