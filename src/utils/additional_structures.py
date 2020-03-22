import random


class Word2vec:
    def get_word_vector(self, word):
        raise Exception('Not implemented')


class FastText(Word2vec):
    def get_word_vector(self, word):
        vector = [ 0 for i in range(300)]
        for i, ch in enumerate(word):
            vector[i] = ord(ch)
        return vector


class _Node:
    def __init__(self, char: str):
        self.char = char
        self.children = {}
        self.value = None


class WordTrie:
    def __init__(self, word2vec:Word2vec):
        self.root = _Node('*')
        self.get_vector = word2vec.get_word_vector

    def add(self, word):
        tmp_node = self.root

        for char in word:
            child = tmp_node.children.get(char, None)
            if child is None:
                child = _Node(char)
                tmp_node.children[char] = child
            tmp_node = child


        tmp_node.value = self.get_vector(word)

    def build_dict(self, words):
        for word in words:
            self.add(word)

    def search_by_prefix(self, prefix):
        pass


# wt = WordTrie(FastText())
# wt.build_dict(['word', 'world', 'cat', 'cats'])
