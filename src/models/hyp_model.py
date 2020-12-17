from wiki_ru_wordnet import WikiWordnet

from src.utils.features_sentence import search_simple_bigramm


class HypWords:
    # hyponym and hypernym words
    def __init__(self, a_tops=10):
        self.wikiwordnet = WikiWordnet()
        self.tops = a_tops

    def _get_hyp_with_prefix(self, word, words_with_prefix):
        hyp_w = get_hyponym_and_hypernym(self.wikiwordnet, word)
        answer = hyp_w & words_with_prefix
        if answer:
            return list(answer)
        return []

    def is_in_vocab(self, word):
        sets = self.wikiwordnet.get_synsets(word)
        return len(sets) != 0

    def get_words(self, query):
        lem_pos_list = query['lem_pos_list']
        bigramm_w = search_simple_bigramm(lem_pos_list)
        words_with_prefix = set(query['words_with_prefix'])
        word = None

        if bigramm_w:
            bigramm = ' '.join(bigramm_w)
            ans = self._get_hyp_with_prefix(bigramm, words_with_prefix)
            if ans:
                return ans[:self.tops]
            word = bigramm_w[1]
        else:
            for w in lem_pos_list:
                if w['pos'] == 'S':
                    word = w['lex']
                    break

        return self._get_hyp_with_prefix(word, words_with_prefix)[:self.tops]


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
