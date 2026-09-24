import csv
import re

INPUT = 'out/ru-lakes.csv'
OUTPUT = 'out/variant1.csv'

pattern = re.compile(r'^озеро\b')

count = 0
result = []
with open(INPUT, encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        name = (row.get('name') or '').strip()
        if name and pattern.match(name):
            count += 1
            result.append((row['@id'], name))

with open(OUTPUT, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['@id', 'name'])
    writer.writerows(result)

print(f'Условие 1: {count}')
