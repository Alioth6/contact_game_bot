from src.utils.dictionary import get_prefix_trie
from .additional_structures import _Node, WordTrie


class SpellChecker:
    def __init__(self, trie=get_prefix_trie(True)):
        self.trie = trie
        self.init_values_before_new_word()

    def __init_values_before_new_word(self):
        self.__min_dist = 100
        self.__closest_str = ""

    def __dfs(self, tmp_node: _Node, word: str, flag: bool) -> None:
        """
        :param tmp_node: current search vertex
        :param word: the word to which we are looking for the closest from the dictionary
        :param flag: if True then an improved version of the Levenshtein's algorithm will be used,
        otherwise, an usual version will be used
        """
        if tmp_node.value is not None:
            vocab_word = tmp_node._get_prefix()
            number_of_cols = len(vocab_word) + 1
            number_of_rows = len(word) + 1 if not flag else 2
            d_levenshtein = [[0] * number_of_cols for i in range(number_of_rows)]
            for i in range(number_of_rows):
                d_levenshtein[i][0] = i
            for j in range(number_of_cols):
                d_levenshtein[0][j] = j
            for i in range(1, len(word) + 1):
                for j in range(1, number_of_cols):
                    delta = int(word[i - 1] != vocab_word[j - 1])
                    curr_row = i if not flag else 1
                    d_levenshtein[curr_row][j] = min(d_levenshtein[curr_row][j - 1] + 1, d_levenshtein[curr_row - 1][j] + 1,
                                                     d_levenshtein[curr_row - 1][j - 1] + delta)
                    if flag:
                        for j in range(number_of_cols):
                            d_levenshtein[0][j] = d_levenshtein[1][j]
                        d_levenshtein[1][0] += 1
            if d_levenshtein[number_of_rows - 1][len(vocab_word)] <= self.min_dist:
                self.min_dist = d_levenshtein[len(word) + 1][len(vocab_word) + 1]
                self.closest_str = vocab_word
        if len(tmp_node.children):
            for child in tmp_node.children.values():
                dfs(self, child, word, flag)

    def search_closest_word(self, word: str, flag: bool) -> str:
        """
        :param word: the word to which we are looking for the closest from the dictionary
        :param flag: bool; if flag == True then an improved version of the Levenshtein's algorithm will be used,
        otherwise, an usual version will be used
        :returns: the word from the dictionary closest to the input param 'word' (Levenshtein's metric)
        """
        self.init_values_before_new_word()
        found_words = [vocab_word for vocab_word, vector in self.trie.search_by_prefix(word)]
        if word in found_words:
            return word
        else:
            self.dfs(self.trie.root, word, flag)
            return self.closest_str
