import os
import csv
import json
from typing import Any
from collections import defaultdict

from .statistics import stats

type dataRow = tuple[str, int, str, str, str, str]


def read_csv(INPUT: str) -> tuple[int, list[dataRow]]:
    data = []
    with open(INPUT, encoding='utf-8-sig') as f:
        for i, row in enumerate(csv.DictReader(f, delimiter=';')):
            data.append(((row.get('@type') or '').strip(),
                         int((row.get('@id') or '0').strip()),
                         (row.get('name') or '').strip(),
                         (row.get('region') or '').strip(),
                         (row.get('@lat') or '').strip(),
                         (row.get('@lon') or '').strip()))
    stats["names_amount"]["all"] = i
    return i, data


def write_csv(data: list[dataRow], output_dir: str, var: Any) -> None:
    os.makedirs(output_dir, exist_ok=True)

    if var == 'exceptions':
        path = os.path.join(output_dir, "exceptions.csv")
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
            path = os.path.join(output_dir, f"{safe_name}.csv")
            with open(path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(
                    ['@type', '@id', 'name', 'region', '@lat', '@lon']
                )
                writer.writerows(rows)


def write_json(data: list[dataRow], output_dir: str, var: Any) -> None:
    os.makedirs(output_dir, exist_ok=True)

    headers = ['@type', '@id', 'name', 'region', '@lat', '@lon']

    if var == 'exceptions':
        path = os.path.join(output_dir, "exceptions.json")
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
            path = os.path.join(output_dir, f"{safe_name}.json")
            records = [dict(zip(headers, row)) for row in rows]
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(records, f, indent=4, ensure_ascii=False)
