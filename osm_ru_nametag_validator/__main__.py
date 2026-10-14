import argparse
import textwrap
import os
import sys

from .api_keys import get_api_keys
from .download_data import download_lakes, download_regions
from .name_checker import name_checker
from .cli_colors import RED, RESET

from .statistics import write_stats


DATA_DIR = 'data'
OUT_DIR = 'out'
LAKES_DATA = os.path.join(DATA_DIR, 'ru-lakes.csv')
REGIONS_DATA = os.path.join(DATA_DIR, 'ru-regions.geojson')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=textwrap.dedent("""
        Анализ тега [name=] озёр из OSM.
        https://community.openstreetmap.org/t/name/148024
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--api', default=os.environ.get("API_KEY"),
                        help='использовать выбранный API ключ для запроса'
                        'Overpass')
    parser.add_argument('--local', action='store_true',
                        help='не скачивать озера, использовать локальный CSV')
    parser.add_argument('--refresh', action='store_true',
                        help='принудительно обновить озера')
    parser.add_argument('--refresh-regions', action='store_true',
                        help='принудительно обновить границы регионов')
    parser.add_argument('--json', action='store_true',
                        help='выводить озера в формате .json вместо .csv')
    parser.add_argument('--out-dir', default=os.environ.get("OUT_DIR"),
                        help='выбрать директорию для вывода')

    args = parser.parse_args()

    if args.refresh and args.local:
        parser.error(f'{RED}Флаги --refresh и --local несовместимы.{RESET}')
    if args.api and args.local:
        parser.error(f'{RED}Флаги --api и --local несовместимы.{RESET}')

    return args


def main() -> None:
    args = parse_args()

    if args.out_dir:
        out_dir = args.out_dir
    else:
        out_dir = OUT_DIR

    stats_file = os.path.join(out_dir, 'stats.json')
    iso_codes_file = os.path.join(out_dir, 'iso-codes.json')

    if (args.refresh or args.refresh_regions or
            not os.path.exists(REGIONS_DATA) or
            not os.path.exists(LAKES_DATA)):
        API = get_api_keys(args.api)

    if args.refresh_regions or not os.path.exists(REGIONS_DATA):
        dir_name = os.path.dirname(REGIONS_DATA)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        download_regions(API, REGIONS_DATA)
    else:
        print(f'Найдены данные регионов [{REGIONS_DATA}]')

    if args.local:
        if not os.path.exists(LAKES_DATA):
            sys.exit(f'{RED}Ошибка: локальный файл {LAKES_DATA} не найден.'
                     '{RESET}')

    elif args.refresh or not os.path.exists(LAKES_DATA):
        dir_name = os.path.dirname(LAKES_DATA)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        download_lakes(API, LAKES_DATA, REGIONS_DATA)
    else:
        print(f'Найдены данные озер [{LAKES_DATA}]')

    name_checker(LAKES_DATA, out_dir, args.json)

    write_stats(stats_file, iso_codes_file, REGIONS_DATA)


if __name__ == '__main__':
    main()
