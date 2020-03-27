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
        self.parent = None

    def _get_prefix(self):
        tmp_node = self
        prefix = ''
        while tmp_node.parent:
            prefix = tmp_node.char + prefix
            tmp_node = tmp_node.parent

        return prefix

    def get_childs(self):
        stack = [(self, self._get_prefix())]

        while stack:
            tmp_node, prefix = stack.pop(0)
            if tmp_node.value:
                yield prefix, tmp_node.value
            
            for char, child in tmp_node.children.items():
                stack.append((child, prefix+char))


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
                child.parent = tmp_node
            tmp_node = child

        tmp_node.value = self.get_vector(word)

    def build_dict(self, words):
        for word in words:
            self.add(word)
        return self

    def search_by_prefix(self, prefix):
        tmp_node = self.root

        for char in prefix:
            tmp_node = tmp_node.children.get(char, None)
            if tmp_node is None:
                return
        yield from tmp_node.get_childs()


# wt = WordTrie(FastText())
# wt.build_dict(['word', 'world', 'cat', 'cats'])
# for word, vector in wt.search_by_prefix('cats'): 
#     print(word)
