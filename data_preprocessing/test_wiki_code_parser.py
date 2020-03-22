#!/usr/bin/env python

"""test_wiki_code_parser.py: Tests for wiki code parser."""

__author__      = "pavlov200912"
__maintainer__  = "Alioth6"


import pytest
import wiki_code_parser as wp


def test_true():
    assert 2 * 2 == 4


def test_remove_html_tags():
    assert wp._remove_html_tags("I Love <html>Really Like</html>") == \
           "I Love Really Like"
    assert wp._remove_html_tags("<text a = \"some text\">Some more Text!</text>") == \
           "Some more Text!"


def test_trim_string():
    assert wp._trim_string(" I love    extra        spaces") == \
           "I love extra spaces"

    assert wp._trim_string("Spaces        to              the mooooooooooooooooon                   ") == \
           "Spaces to the mooooooooooooooooon"


def test_remove_accents():
    assert wp._remove_accents("Уда́ре́ни́я́ пло́хо́!") == \
           "Ударения плохо!"


def test_clean_string():
    assert wp.clean_string("I like \ backslash \ a lot \\") == \
           "I like backslash a lot"


def test_clean_wikilist():
    text = """
    # [[искусственный]] [[водоём]] 
    # {{гидрол.|ru}} совокупность рек
    # {{гелог.|ru}} бассейн Волги
    """
    assert wp.clean_wikilist(text, '[#*,]') == \
           ["искусственный водоём", "совокупность рек", "бассейн Волги"]

    text = """
    * [[text]] with text
    * {{some template|some nested text}} pure text
    """

    assert wp.clean_wikilist(text, '[#*,]') == \
           ["text with text", "pure text"]


def test_clean_meanings():
    text = """
        # [[искусственный]] [[водоём]] {{пример| У меня в деревне был {{выдел|бассейн}} }}
        # {{гидрол.|ru}} совокупность рек {{пример| бассейн Ленинградской области {{выдел|страдал}} от нехватки рыбы}}"
        # {{гелог.|ru}} Какая-то геологическая штука {{пример|бассейн {{выдел|Волги}} }}
        """
    assert wp.clean_meanings(text) == \
           [("искусственный водоём", ["У меня в деревне был бассейн"]),
            ("совокупность рек", ["бассейн Ленинградской области страдал от нехватки рыбы"]),
            ("Какая-то геологическая штука", ["бассейн Волги"])]


def test_validate_title():
    assert not wp.validate_title("Some english title")
    assert not wp.validate_title("Справка:Помощь")
    assert not wp.validate_title("213")
    assert not wp.validate_title("???")
    assert wp.validate_title("Слон")


def test_validate_text():
    assert not wp.validate_text("This is #REDIRECT page")
    assert wp.validate_text("Страница про Слона")


def test_chunks():
    gen_1 = wp.chunks([1, 2, 3, 4], 2)
    list_1 = [[1, 2], [3, 4]]
    assert all(a == b for a, b in zip(gen_1, list_1))
    gen_2 = wp.chunks([1, 2, 3, 4, 5], 2)
    list_2 = [[1, 2], [3, 4], [5]]
    assert all(a == b for a, b in zip(gen_2, list_2))


if __name__ == "__main__":
    pytest.main()
