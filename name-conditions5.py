import csv
import re

INPUT = 'ru-lakes.csv'
OUTPUT = 'names-condition5.csv'

TOKEN = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)?")
GENERIC = {'озеро', 'озера', 'озёра'}


def has_generic(tokens):
    return any(
        t.lower() in GENERIC and (t.islower() or i == 0)
        for i, t in enumerate(tokens)
    )


def matches(name):
    """Подходит любое имя без родового слова "озеро"."""
    for variant in name.split('/'):
        tokens = TOKEN.findall(variant.strip())
        if tokens and not has_generic(tokens):
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

print(f'Условие 5: {count}')
