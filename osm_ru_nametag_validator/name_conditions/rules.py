from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer()


def name_type(word):
    if morph.word_is_known(word):
        for p in morph.parse(word):
            if p.tag.POS == 'ADJS':
                return 'substant'
            if p.tag.POS == 'NOUN' and p.tag.case == 'gent':
                return 'gent'

    for p in morph.parse(word):
        if p.tag.POS == 'NOUN' and 'Geox' in p.tag:
            return 'substant'
        if (p.tag.POS == 'ADJF'
                and 'Fixd' not in p.tag):
            return 'adjf'
        if 'Surn' in p.tag and p.tag.case == 'gent':
            return 'gent'

        # if ('Surn' in p.tag
        #         and 'Fixd' not in p.tag
        #         and p.tag.number == 'plur'
        #         and p.tag.case == 'nomn'):
        #     return 'adjf'
