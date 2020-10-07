from src.utils.dictionary import get_prefix_trie


class Spell_checker:
    def __init__(self):
        self.trie = get_prefix_trie(True)

    def search_closest_word(self, word, flag):
        # flag indicates whether to use an improved version of the Levenshtein's algorithm
        found_words = [vocab_word for vocab_word, vector in self.trie.search_by_prefix(word)]
        if word in found_words:
            return word
        else:
            min_dist = 100
            closest_str = ""
            for vocab_word in self.trie.all_words:
                number_of_cols = len(vocab_word) + 1
                number_of_rows = len(word) + 1 if not flag else 2
                d_levenshtein = [[0] * number_of_cols for i in range(number_of_rows)]
                for i in range(number_of_rows):
                    d_levenshtein[i][0] = i
                for j in range(number_of_cols):
                    d_levenshtein[0][j] = j
                for i in range(1, len(word) + 1):
                    for j in range(1, number_of_cols):
                        delta = 0
                        if word[i - 1] == vocab_word[j - 1]:
                            delta = 1
                        curr_row = i if not flag else 1
                        d_levenshtein[curr_row][j] = min(d_levenshtein[curr_row][j - 1], d_levenshtein[curr_row - 1][j],
                                                         d_levenshtein[curr_row - 1][j - 1] + delta)
                        if flag:
                            for j in range(number_of_cols):
                                d_levenshtein[0][j] = d_levenshtein[1][j]
                            d_levenshtein[1][0] += 1
                if d_levenshtein[number_of_rows][len(vocab_word) + 1] <= min_dist:
                    min_dist = d_levenshtein[len(word) + 1][len(vocab_word) + 1]
                    closest_str = vocab_word
            return closest_str
