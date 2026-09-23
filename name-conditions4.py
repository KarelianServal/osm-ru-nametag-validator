import csv
import re
from pymorphy3 import MorphAnalyzer

INPUT = 'ru-lakes.csv'
OUTPUT = 'names-condition4.csv'

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
    """B: прил. + озеро | C: "озеро" внутри имени | D: сущ. без "озеро"."""
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
            if (generic_idx == [len(tokens) - 1] and rest
                    and all(is_adj(t) for t in rest)):
                return True
        elif embedded:
            return True
        elif any(is_noun(t) for t in tokens):
            return True
    return False


count = 0
result = []
with open(INPUT, encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        name = (row.get('name') or '').strip()
        if name and matches(name):
            count += 1
            result.append((row['@id'], name))

with open(OUTPUT, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['@id', 'name'])
    writer.writerows(result)

print(f'Условие 4: {count}')
