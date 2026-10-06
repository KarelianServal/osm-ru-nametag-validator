import csv

from .name_conditions import VARIANTS
from .name_conditions.exceptions import is_exception


def count_names(path):
    with open(path, encoding='utf-8-sig') as f:
        return sum(
            1 for row in csv.DictReader(f)
            if (row.get('name') or '').strip()
        )


def read_csv(INPUT, condition):
    count = 0
    valid_result = []
    invalid_result = []

    with open(INPUT, encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
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


def find_valid_names(data, condition):
    count = 0
    valid_result = []
    invalid_result = []

    for (osm_type,
         osm_id,
         osm_name,
         osm_region,
         osm_lat,
         osm_lon) in data:
        if condition(osm_name):
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


def write_csv(data, OUTPUT):
    with open(OUTPUT, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['@type',
                         '@id',
                         'name',
                         'region',
                         '@lat',
                         '@lon'])
        writer.writerows(data)


def name_checker(INPUT, DATA_FOLDER):
    total = count_names(INPUT)

    (exeptions_amount,
     valid_exceptions,
     valid_names) = read_csv(INPUT, is_exception)

    write_csv(valid_exceptions, DATA_FOLDER + 'exceptions.csv')

    pct = round(exeptions_amount / total * 100) if total else 0
    print(f'Исключения: {exeptions_amount}/{total} ({pct}%)')

    total -= exeptions_amount

    for i, is_variant in enumerate(VARIANTS):
        (valid_names_amount,
         valid_data,
         invalid_data) = find_valid_names(valid_names, is_variant)

        OUTPUT = [DATA_FOLDER + f'variant{i+1}-names.csv',
                  DATA_FOLDER + f'variant{i+1}-invalid-names.csv']

        write_csv(valid_data, OUTPUT[0])
        write_csv(invalid_data, OUTPUT[1])

        pct = round(valid_names_amount / total * 100) if total else 0
        print(f'Условие {i+1}: {valid_names_amount}/{total} ({pct}%)')
