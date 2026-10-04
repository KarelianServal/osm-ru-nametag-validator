import re

from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer()

noun_patterns = re.compile(r'(ын)$')


def name_type(word):
    if morph.word_is_known(word):
        for p in morph.parse(word):
            if p.tag.POS == 'ADJS':
                return 'substant'
            if p.tag.POS == 'NOUN' and p.tag.case == 'gent':
                return 'gent'

    if noun_patterns.search(word):
        return 'noun'

    for p in morph.parse(word):
        if p.tag.POS == 'NOUN' and 'Geox' in p.tag:
            return 'substant'
        if 'Surn' in p.tag and p.tag.case == 'gent':
            return 'gent'
        if (p.tag.POS == 'ADJF'
                and 'Fixd' not in p.tag):
            return 'adjf'

    return 'noun'
