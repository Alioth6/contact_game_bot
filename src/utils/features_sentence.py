import pymorphy2


morph = pymorphy2.MorphAnalyzer()


def search_simple_bigramm(lemma_list):
    if not lemma_list:
        return

    for w1, w2 in zip(lemma_list, lemma_list[1:]):
        if w1['pos']=='A' and w2['pos']=='S':
            # parsing word - receiving list of possible values
            w1_vars = morph.parse(w1['lex'])
            # choosing elements with compatible POS
            w1_vars = [i for i in w1_vars if i.tag.POS == 'ADJF']

            word2 = w2['lex']
            w2_vars = morph.parse(word2)
            w2_vars = [i for i in w2_vars if i.tag.POS == 'NOUN']

            if len(w1_vars) == 0 or len(w2_vars) == 0:
                return
            gender = w2_vars[0].tag.gender

            try:
                word1 = w1_vars[0].inflect({gender}).word
            except ValueError:
                word1 = w1_vars[0].word
            return word1, word2
