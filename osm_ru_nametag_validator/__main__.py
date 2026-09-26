import argparse
import textwrap
import os
import sys

from .download_data import download_data
from .name_checker import name_checker
from .cli_colors import RED, RESET


DATA_FOLDER = 'out/'
INPUT = DATA_FOLDER + 'ru-lakes.csv'


def parse_args():
    parser = argparse.ArgumentParser(
                description=textwrap.dedent("""
                Анализ тега [name=] озёр из OSM.
                https://community.openstreetmap.org/t/name/148024
                """),
                formatter_class=argparse.RawDescriptionHelpFormatter
             )

    parser.add_argument('--refresh', action='store_true',
                        help='принудительно скачать свежие данные')
    parser.add_argument('--local', action='store_true',
                        help='не скачивать, использовать локальный CSV')
    parser.add_argument('--api', default=os.environ.get("API_KEY"),
                        help='использовать выбранный API ключ для запроса Overpass')

    args = parser.parse_args()

    if args.refresh and args.local:
        parser.error(f'{RED}Флаги --refresh и --local несовместимы.{RESET}')
    if args.api and args.local:
        parser.error(f'{RED}Флаги --api и --local несовместимы.{RESET}')

    return args


def main():

    args = parse_args()

    if args.local:
        if not os.path.exists(INPUT):
            sys.exit(f'{RED}Ошибка: локальный файл {INPUT} не найден.{RESET}')

    elif args.refresh or not os.path.exists(INPUT):
        dir_name = os.path.dirname(INPUT)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        download_data(args.api, INPUT)

    name_checker(INPUT, DATA_FOLDER)


if __name__ == '__main__':
    main()
