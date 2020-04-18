import pymorphy2


morph = pymorphy2.MorphAnalyzer()


def search_simple_bigramm(lemma_list):
    if not lemma_list:
        return

    for w1, w2 in zip(lemma_list, lemma_list[1:]):
        if w1['pos']=='A' and w2['pos']=='S':
            w2 = w2['lex']
            gender = morph.parse(w2)[0].tag.gender 
            w1 = morph.parse(w1['lex'])[0].inflect({gender})
            return w1.word, w2
