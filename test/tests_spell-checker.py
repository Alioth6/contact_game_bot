import spell_checker
import pywin32_testutil
from .additional_structures import WordTrie, FastText


wt = WordTrie(FastText())
wt.build_dict(['киллер', 'килобайт', 'кинематика', 'кино', 'кинотеатр', 'кинза', 'кинжал'])


def test(flag, word, expected):
    a = Spell_checker(wt)
    output = a.search_closest_word(word, flag)
    assert expected == output


test(0, "кно", "кино")
test(1, "кно", "кино")
test(0, "конематкиа", "кинематика")
test(1, "конематкиа", "кинематика")