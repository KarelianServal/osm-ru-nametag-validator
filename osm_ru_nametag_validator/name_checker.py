import os
from collections import defaultdict
from collections.abc import Callable

from .name_conditions import VARIANTS
from .name_conditions.exceptions import is_exception
from .names_io import read_csv, write_csv, write_json

from .statistics import stats

type dataRow = tuple[str, int, str, str, str, str]


def _pct(some: int, all: int) -> int:
    return round(some / all * 100) if all else 0


def _find_regions_amount(data: list[dataRow]) -> None:
    groups = defaultdict(list)
    for row in data:
        region = row[3]
        groups[region].append(row)

    for region, rows in groups.items():
        stats["names_amount"]["region"][region] = len(rows)


def _find_valid_names(
        data: list[dataRow],
        condition: Callable[[str], bool]
) -> tuple[int, list[dataRow], list[dataRow]]:
    valid: list[dataRow] = []
    invalid: list[dataRow] = []

    for row in data:
        (valid if condition(row[2]) else invalid).append(row)

    return len(valid), valid, invalid


def _find_exceptions(
        data: list[dataRow]
) -> tuple[int, list[dataRow], list[dataRow]]:
    valid: list[dataRow] = []
    invalid: list[dataRow] = []

    for row in data:
        (valid if is_exception(row[0], row[1], row[2])
         else invalid).append(row)

    return len(valid), valid, invalid


def name_checker(INPUT: str, OUTPUT_DIR: str, is_json: bool) -> None:
    total_amount, all_names = read_csv(INPUT)

    # Exceptions
    (exceptions_amount,
     exceptions,
     valid_names) = _find_exceptions(all_names)

    if is_json:
        write_json(exceptions, OUTPUT_DIR, 'exceptions')
    else:
        write_csv(exceptions, OUTPUT_DIR, 'exceptions')

    pct = _pct(exceptions_amount, total_amount)
    print(f'Исключения: {exceptions_amount}/{total_amount} ({pct}%)')
    stats["exceptions"]["amount"] = exceptions_amount

    valid_amount = total_amount - exceptions_amount
    stats["names_amount"]["legal"] = valid_amount

    # Stats
    _find_regions_amount(valid_names)

    # Variants
    for var, is_variant in enumerate(VARIANTS, start=1):
        (var_amount,
         var_valid_names,
         var_invalid_names) = _find_valid_names(valid_names,
                                                is_variant)
        pct = _pct(var_amount, valid_amount)
        print(f'Условие {var}: {var_amount}/{valid_amount} ({pct}%)')
        stats["variant"][var]["amount"] = var_amount

        variant_dir = [os.path.join(OUTPUT_DIR, f'valid-variant{var}'),
                       os.path.join(OUTPUT_DIR, f'invalid-variant{var}')]

        if is_json:
            write_json(var_valid_names, variant_dir[0], var)
            write_json(var_invalid_names, variant_dir[1], None)
        else:
            write_csv(var_valid_names, variant_dir[0], var)
            write_csv(var_invalid_names, variant_dir[1], None)
