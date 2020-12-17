from pymystem3 import Mystem
import re


class Text2Lemms:
    def __init__(self, a_spell_checker=None):
        self.stemmer = Mystem()
        self.spell_checker = a_spell_checker

    def get_lemms(self, raw_text, tag_to_get=None):
        lemms_list = []
        checked_text = '' if self.spell_checker else raw_text

        # check if there are non dictionary words
        # replace them with spell checker
        if self.spell_checker:
            for entry in self.stemmer.analyze(raw_text):
                chunk = entry['text']
                if 'analysis' in entry and len(entry['analysis']):
                    analysis = entry['analysis'][0]
                    if analysis.get('qual', None) == 'bastard':
                        chunk = self.spell_checker.search_closest_word(chunk.lower(), 1)
                checked_text += chunk

        # make the list of significant words and its PoS tags
        for entry in self.stemmer.analyze(checked_text):
            if 'analysis' in entry and len(entry['analysis']):
                analysis = entry['analysis'][0]
                if analysis.get('qual', None) == 'bastard':
                    continue
                pos_tag = re.match('[A-Z]+', analysis['gr']).group(0)
                if tag_to_get and pos_tag == tag_to_get:
                    lemms_list.append(analysis['lex'])
                elif not tag_to_get:
                    lemms_list.append({'lex': analysis['lex'], 'pos': pos_tag})

        return lemms_list
