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


# Родительный падеж
def is_gent(word):
    word = word.rpartition('-')[-1]
    for p in morph.parse(word):
        if p.tag.POS == 'NOUN':
            return p.tag.case == 'gent'


def matches(name):
    for variant in name.split('/'):
        tokens = TOKEN.findall(variant.strip())

        if any(t in OZERO for t in tokens):
            if len(tokens) < 2:
                raise RuntimeError(f'Неверное имя - {tokens[0]}')

            if tokens[-1] in OZERO:
                if is_adjf(tokens[-2]) and not is_gent(tokens[-2]):
                    return True
            if tokens[0] in OZERO:
                if not is_adjf(tokens[-1]) or is_gent(tokens[-1]):
                    return True

    return False


def is_variant2(lake_name):
    return lake_name and matches(lake_name)
