import re
from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer()
TOKEN = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)?")
OZERO = {'озеро', 'озера', 'озёра'}

# Edge-cases
unique = {
}


# Прилагательные
def is_adjf(word):
    for p in morph.parse(word):
        if p.tag.POS in ('ADJF', 'ADJS'):
            return True


# Родительный падеж
def is_gent(word):
    word = word.rpartition('-')[-1]
    for p in morph.parse(word):
        if p.tag.POS == 'NOUN':
            return p.tag.case == 'gent'


def matches(name):
    for variant in name.split('/'):
        tokens = TOKEN.findall(variant.strip())
        if len(tokens) < 2:
            if not is_adjf(tokens[0]) and not is_gent(tokens[0]):
                return True
            else:
                continue
        if tokens[-1] in OZERO and is_adjf(tokens[-2]):
            return True
        if tokens[0] in OZERO:
            if is_gent(tokens[-1]):
                return True
        else:
            if not is_adjf(tokens[-1]) and not is_gent(tokens[-1]):
                return True

    return False


def is_variant4(lake_name):
    return lake_name and matches(lake_name)
