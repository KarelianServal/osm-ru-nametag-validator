import re

TOKEN = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)?")
OZERO = {'озеро', 'озера', 'озёра'}


def has_generic(tokens):
    return any(
        t.lower() in OZERO and (t.islower() or i == 0)
        for i, t in enumerate(tokens)
    )


def matches(name):
    for variant in name.split('/'):
        tokens = TOKEN.findall(variant.strip())
        if tokens and not has_generic(tokens):
            return True
    return False


def is_variant5(lake_name):
    if lake_name and matches(lake_name):
        return True
    else:
        return False
