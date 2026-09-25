import re
from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer()
TOKEN = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)?")
OZERO = {'озеро', 'озера', 'озёра'}


def pos_of(word):
    return morph.parse(word)[0].tag.POS


def is_noun(word):
    return pos_of(word) in (None, 'NOUN')


def is_adj(word):
    return pos_of(word) in ('ADJF', 'PRTF')


def matches(name):
    """A: озеро + существительное | B: прилагательные + озеро."""
    for variant in name.split('/'):
        tokens = TOKEN.findall(variant.strip())
        low = [t.lower() for t in tokens]
        if len(tokens) < 2:
            continue
        if low[0] in OZERO and any(is_noun(t) for t in tokens[1:]):
            return True
        if low[-1] in OZERO and all(is_adj(t) for t in tokens[:-1]):
            return True
    return False


def is_variant2(lake_name):
    if lake_name and matches(lake_name):
        return True
    else:
        return False
