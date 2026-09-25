import re
from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer()
TOKEN = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)?")
GENERIC = {'озеро', 'озера', 'озёра'}


def is_compound(token):
    t = token.lower().replace('ё', 'е')
    return t.endswith('озеро') and t not in GENERIC


def pos_of(word):
    return morph.parse(word)[0].tag.POS


def is_noun(word):
    return pos_of(word) in (None, 'NOUN')


def is_adj(word):
    return pos_of(word) in ('ADJF', 'PRTF')


def matches(name):
    """A: озеро + сущ. | B: прил. + озеро | C: "озеро" внутри имени."""
    for variant in name.split('/'):
        tokens = TOKEN.findall(variant.strip())
        if not tokens:
            continue
        generic_idx = [
            i for i, t in enumerate(tokens)
            if t.lower() in GENERIC and (t.islower() or i == 0)
        ]
        embedded = any(is_compound(t) for t in tokens) or any(
            t.lower() in GENERIC and not t.islower() and i != 0
            for i, t in enumerate(tokens)
        )
        if generic_idx:
            if embedded:
                continue  # тавтология
            rest = [t for i, t in enumerate(tokens) if i not in generic_idx]
            if generic_idx == [0] and any(is_noun(t) for t in rest):
                return True
            if generic_idx == [len(tokens) - 1] and all(
                    is_adj(t) for t in rest):
                return True
        elif embedded:
            return True
    return False


def is_variant3(lake_name):
    if lake_name and matches(lake_name):
        return True
    else:
        return False
