import os
import csv
import json
from typing import Any
from collections import defaultdict
from collections.abc import Callable

from .name_conditions import VARIANTS
from .name_conditions.exceptions import is_exception

from .statistics import stats


def _count_names(path: str) -> int:
    with open(path, encoding='utf-8-sig') as f:
        return sum(
            1 for row in csv.DictReader(f, delimiter=';')
            if (row.get('name') or '').strip()
        )


def _find_regions_amount(
        data: list[tuple[str, int, str, str, str, str]]
) -> None:
    groups = defaultdict(list)
    for row in data:
        region = row[3]
        groups[region].append(row)

    for region, rows in groups.items():
        stats["names_amount"]["region"][region] = len(rows)


def read_csv(
        INPUT: str,
        condition: Callable[[str, int, str], bool]
) -> tuple[int,
           list[tuple[str, int, str, str, str, str]],
           list[tuple[str, int, str, str, str, str]]]:
    count = 0
    valid_result = []
    invalid_result = []

    with open(INPUT, encoding='utf-8-sig') as f:
        for row in csv.DictReader(f, delimiter=';'):
            osm_type = (row.get('@type') or '').strip()
            osm_id = int((row.get('@id') or '').strip())
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


def read_valid_names(
        data: list[tuple[str, int, str, str, str, str]],
        condition: Callable[[str], bool]
) -> tuple[int,
           list[tuple[str, int, str, str, str, str]],
           list[tuple[str, int, str, str, str, str]]]:
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


def write_csv(
        data: list[tuple[str, int, str, str, str, str]],
        OUTPUT_DIR: str,
        var: Any
) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if var == 'exceptions':
        path = os.path.join(OUTPUT_DIR, "exceptions.csv")
        with open(path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['@type', '@id', 'name', 'region', '@lat', '@lon'])
            writer.writerows(data)

    else:
        groups = defaultdict(list)
        for row in data:
            region = row[3]
            groups[region].append(row)

        for region, rows in groups.items():
            if region and var:
                stats["variant"][var]["region"][region]["amount"] = len(rows)

            safe_name = region.replace('/', '_').replace('\\', '_')
            path = os.path.join(OUTPUT_DIR, f"{safe_name}.csv")
            with open(path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(
                    ['@type', '@id', 'name', 'region', '@lat', '@lon']
                )
                writer.writerows(rows)


def write_json(
        data: list[tuple[str, int, str, str, str, str]],
        OUTPUT_DIR: str,
        var: Any
) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    headers = ['@type', '@id', 'name', 'region', '@lat', '@lon']

    if var == 'exceptions':
        path = os.path.join(OUTPUT_DIR, "exceptions.json")
        records = [dict(zip(headers, row)) for row in data]
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=4, ensure_ascii=False)

    else:
        groups = defaultdict(list)
        for row in data:
            region = row[3]
            groups[region].append(row)

        for region, rows in groups.items():
            if region and var:
                stats["variant"][var]["region"][region]["amount"] = len(rows)

            safe_name = region.replace('/', '_').replace('\\', '_')
            path = os.path.join(OUTPUT_DIR, f"{safe_name}.json")
            records = [dict(zip(headers, row)) for row in rows]
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(records, f, indent=4, ensure_ascii=False)


def name_checker(INPUT: str, OUT_DIR: str, is_json: bool) -> None:
    total = _count_names(INPUT)
    stats["names_amount"]["all"] = total

    (exceptions_amount,
     valid_exceptions,
     valid_names) = read_csv(INPUT, is_exception)

    if is_json:
        write_json(valid_exceptions, OUT_DIR, 'exceptions')
    else:
        write_csv(valid_exceptions, OUT_DIR, 'exceptions')

    pct = round(exceptions_amount / total * 100) if total else 0
    print(f'Исключения: {exceptions_amount}/{total} ({pct}%)')
    stats["exceptions"]["amount"] = exceptions_amount

    legal = total - exceptions_amount
    stats["names_amount"]["legal"] = legal

    _find_regions_amount(valid_names)

    for i, is_variant in enumerate(VARIANTS, start=1):
        (valid_names_amount,
         valid_data,
         invalid_data) = read_valid_names(valid_names, is_variant)

        VARIANT_DIR = [os.path.join(OUT_DIR, f'valid-variant{i}'),
                       os.path.join(OUT_DIR, f'invalid-variant{i}')]

        if is_json:
            write_json(valid_data, VARIANT_DIR[0], i)
            write_json(invalid_data, VARIANT_DIR[1], None)
        else:
            write_csv(valid_data, VARIANT_DIR[0], i)
            write_csv(invalid_data, VARIANT_DIR[1], None)

        pct = round(valid_names_amount / legal * 100) if legal else 0
        print(f'Условие {i}: {valid_names_amount}/{legal} ({pct}%)')

        stats["variant"][i]["amount"] = valid_names_amount
