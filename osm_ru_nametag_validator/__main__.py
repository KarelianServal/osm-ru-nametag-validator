import argparse
import textwrap
import os
import sys

from .api_keys import get_api_keys
from .download_data import download_lakes
from .name_checker import name_checker
from .cli_colors import RED, RESET


DATA_FOLDER = 'out/'
LAKES_DATA = DATA_FOLDER + 'ru-lakes.csv'


def parse_args():
    parser = argparse.ArgumentParser(
                description=textwrap.dedent("""
                Анализ тега [name=] озёр из OSM.
                https://community.openstreetmap.org/t/name/148024
                """),
                formatter_class=argparse.RawDescriptionHelpFormatter
             )

    parser.add_argument('--api', default=os.environ.get("API_KEY"),
                        help='использовать выбранный API ключ для запроса Overpass')
    parser.add_argument('--local', action='store_true',
                        help='не скачивать озера, использовать локальный CSV')
    parser.add_argument('--refresh', action='store_true',
                        help='принудительно обновить озера')

    args = parser.parse_args()

    if args.refresh and args.local:
        parser.error(f'{RED}Флаги --refresh и --local несовместимы.{RESET}')
    if args.api and args.local:
        parser.error(f'{RED}Флаги --api и --local несовместимы.{RESET}')

    return args


def main():
    args = parse_args()

    if (args.refresh or not os.path.exists(LAKES_DATA)):
        API = get_api_keys(args.api)

    if args.local:
        if not os.path.exists(LAKES_DATA):
            sys.exit(f'{RED}Ошибка: локальный файл {LAKES_DATA} не найден.{RESET}')

    elif args.refresh or not os.path.exists(LAKES_DATA):
        dir_name = os.path.dirname(LAKES_DATA)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        download_lakes(API, LAKES_DATA)

    name_checker(LAKES_DATA, DATA_FOLDER)


if __name__ == '__main__':
    main()
