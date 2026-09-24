import csv
import re
from pymorphy3 import MorphAnalyzer

INPUT = 'out/ru-lakes.csv'
OUTPUT = 'out/variant2.csv'

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

print(f'Условие 2: {count}')
