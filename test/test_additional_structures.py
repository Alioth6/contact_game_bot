import unittest
from src.utils.additional_structures import WordTrie
from src.utils.dictionary import fastTextModel


class WordTrieTestCase(unittest.TestCase):
    def setUp(self):
        self.word_trie = WordTrie(fastTextModel)
        self.words = ['кот', 'котлета', 'котел', 'котангенс', 'коммуналка', 'кино', 'лань']
        self.word_trie.build_dict(self.words)

    def test_build_dict(self):
        trie_w =  self.word_trie.search_by_prefix('')
        result = {w[0] for w in trie_w}
        self.assertEqual(set(self.words), result)

    def test_add(self):
        word = 'комната'
        self.word_trie.add(word)
        trie_w =  self.word_trie.search_by_prefix(word)
        result = {w[0] for w in trie_w}
        self.assertIn(word, result)

    def test_search_by_prefix(self):
        list_data = [
            ('кот', {'кот', 'котлета', 'котел', 'котангенс'}),
            ('л', {'лань'}),
            ('ко', {'кот', 'котлета', 'котел', 'котангенс', 'коммуналка'})
        ]

        for prefix, true_result in list_data:
            trie_w =  self.word_trie.search_by_prefix(prefix)
            result = {w[0] for w in trie_w}
            self.assertEqual(true_result, result)

if __name__ == '__main__':
    unittest.main()
