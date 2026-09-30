from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer()


# Топоним или прилагательное
def is_geox_or_adjf(word):
    for p in morph.parse(word):
        if p.tag.POS == 'NOUN' and 'Geox' in p.tag:
            return 'geox'
        if (p.tag.POS == 'ADJF'
                and 'Fixd' not in p.tag):
            return 'adjf'
    if morph.word_is_known(word):
        for p in morph.parse(word):
            if p.tag.POS == 'ADJS':
                return 'adjf'


# Родительный падеж
def is_gent(word):
    if morph.word_is_known(word):
        for p in morph.parse(word):
            if p.tag.POS == 'NOUN':
                return p.tag.case == 'gent'
    else:
        return any('Surn' in p.tag for p in morph.parse(word))
