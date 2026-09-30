import re
from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer()
TOKEN = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)?")
OZERO = {'озеро', 'озера', 'озёра'}


# Прилагательные
def is_adjf(word):
    for p in morph.parse(word):
        if p.tag.POS in ('ADJF', 'ADJS'):
            return True


def matches(name):
    for variant in name.split('/'):
        tokens = TOKEN.findall(variant.strip())
        if len(tokens) < 2:
            continue
        if tokens[-1] in OZERO and is_adjf(tokens[-2]):
            return True
        if tokens[0] in OZERO and not is_adjf(tokens[-1]):
            return True
    return False


def is_variant2(lake_name):
    return lake_name and matches(lake_name)
