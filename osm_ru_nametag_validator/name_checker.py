import csv
import os
from collections import defaultdict


from .name_conditions import VARIANTS
from .name_conditions.exceptions import is_exception


def count_names(path):
    with open(path, encoding='utf-8-sig') as f:
        return sum(
            1 for row in csv.DictReader(f, delimiter=';')
            if (row.get('name') or '').strip()
        )

def read_csv(INPUT, condition):
    count = 0
    valid_result = []
    invalid_result = []

    with open(INPUT, encoding='utf-8-sig') as f:
        for row in csv.DictReader(f, delimiter=';'):
            osm_type = (row.get('@type') or '').strip()
            osm_id = (row.get('@id') or '').strip()
            osm_name = (row.get('name') or '').strip()
            osm_region = (row.get('region') or '').strip()
            osm_lat = (row.get('@lat') or '').strip()
            osm_lon = (row.get('@lon') or '').strip()

            if condition(osm_type, osm_id, osm_name):
                count += 1
                valid_result.append((osm_type,
                                     osm_id,
                                     osm_name,
                                     osm_region,
                                     osm_lat,
                                     osm_lon))
            else:
                invalid_result.append((osm_type,
                                       osm_id,
                                       osm_name,
                                       osm_region,
                                       osm_lat,
                                       osm_lon))
    return count, valid_result, invalid_result


def read_valid_names(data, condition):
    count = 0
    valid_result = []
    invalid_result = []

    for osm_type, osm_id, name, region, lat, lon in data:
        if condition(name):
            count += 1
            valid_result.append((osm_type,
                                 osm_id,
                                 name,
                                 region,
                                 lat,
                                 lon))
        else:
            invalid_result.append((osm_type,
                                   osm_id,
                                   name,
                                   region,
                                   lat,
                                   lon))
    return count, valid_result, invalid_result


def write_csv(data, OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    groups = defaultdict(list)
    for row in data:
        region = row[3]
        groups[region].append(row)

    for region, rows in groups.items():
        safe_name = region.replace('/', '_').replace('\\', '_')
        path = os.path.join(OUTPUT_DIR, f"{safe_name}.csv")
        with open(path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['@type', '@id', 'name', 'region', '@lat', '@lon'])
            writer.writerows(rows)


def name_checker(INPUT, OUT_DIR):
    total = count_names(INPUT)

    (exeptions_amount,
     valid_exceptions,
     valid_names) = read_csv(INPUT, is_exception)

    write_csv(valid_exceptions, os.path.join(OUT_DIR, 'exceptions'))

    pct = round(exeptions_amount / total * 100) if total else 0
    print(f'Исключения: {exeptions_amount}/{total} ({pct}%)')

    total -= exeptions_amount

    for i, is_variant in enumerate(VARIANTS):
        (valid_names_amount,
         valid_data,
         invalid_data) = read_valid_names(valid_names, is_variant)

        VARIANT_DIR = [os.path.join(OUT_DIR, f'valid-variant{i+1}'),
                       os.path.join(OUT_DIR, f'invalid-variant{i+1}')]

        for t, data in enumerate((valid_data, invalid_data)):
            write_csv(data, VARIANT_DIR[t])

        pct = round(valid_names_amount / total * 100) if total else 0
        print(f'Условие {i+1}: {valid_names_amount}/{total} ({pct}%)')
