import csv

from .name_conditions import VARIANTS


def count_total_names(path):
    with open(path, encoding='utf-8-sig') as f:
        return sum(
            1 for row in csv.DictReader(f)
            if (row.get('name') or '').strip()
        )


def read_csv(INPUT, variant_valid):
    count = 0
    result = []

    with open(INPUT, encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            name = (row.get('name') or '').strip()

            if variant_valid(name):
                count += 1
                result.append((row['@id'], name))
    return count, result


def write_csv(data, OUTPUT):
    with open(OUTPUT, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['@id', 'name'])
        writer.writerows(data)


def name_checker(INPUT, DATA_FOLDER):
    total = count_total_names(INPUT)

    for i, variant_valid in enumerate(VARIANTS):
        valid_names_amount, data = read_csv(INPUT, variant_valid)

        OUTPUT = DATA_FOLDER + f'variant{i}-names.csv'
        write_csv(data, OUTPUT)

        pct = round(valid_names_amount / total * 100) if total else 0
        print(f'Условие {i+1}: {valid_names_amount}/{total} ({pct}%)')
