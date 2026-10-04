import re

from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer()

# pymorphy hallucination workaround:
noun_patterns = re.compile(r'(ын)$')


def is_gent(word, tokens):
    # Workaround for "Две Сестры" cases
    if len(tokens) == 1:
        return True
    else:
        second_word = morph.parse(tokens[-2])[0]

        if second_word.tag.POS == 'NUMR':
            return word.tag.number == 'plur'
        else:
            return word.tag.number == second_word.tag.number


def name_type(tokens):
    word = tokens[-1]

    if morph.word_is_known(word):
        for p in morph.parse(word):
            if p.tag.POS == 'ADJS':
                return 'substant'
            if p.tag.POS == 'NOUN' and p.tag.case == 'gent':
                if is_gent(p, tokens):
                    return 'gent'

    if noun_patterns.search(word):
        return 'noun'

    for p in morph.parse(word):
        if p.tag.POS == 'NOUN' and 'Geox' in p.tag:
            return 'substant'
        if 'Surn' in p.tag and p.tag.case == 'gent':
            if is_gent(p, tokens):
                return 'gent'
        if (p.tag.POS == 'ADJF'
                and 'Fixd' not in p.tag):
            return 'adjf'

    return 'noun'
