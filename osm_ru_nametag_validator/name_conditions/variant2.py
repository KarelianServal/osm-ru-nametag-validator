import re
from .rules import is_geox_or_adjf, is_gent

TOKEN = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)?")
OZERO = {'озеро', 'озера', 'озёра'}


def matches(name):
    for variant in name.split('/'):
        tokens = TOKEN.findall(variant.strip())

        if any(t in OZERO for t in tokens):
            if len(tokens) < 2:
                raise RuntimeError(f'Неверное имя - {tokens[0]}')

            if tokens[-1] in OZERO:
                if is_geox_or_adjf(tokens[-2]) == 'geox':
                    return False
                if (is_geox_or_adjf(tokens[-2]) == 'adjf' and
                        not is_gent(tokens[-2])):
                    return True
            if tokens[0] in OZERO:
                if is_geox_or_adjf(tokens[-1]) == 'geox':
                    return True
                if not is_geox_or_adjf(tokens[-1]) or is_gent(tokens[-1]):
                    return True

    return False


def is_variant2(lake_name):
    return lake_name and matches(lake_name)
