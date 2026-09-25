import argparse
import textwrap
import os
import sys

from osm_ru_nametag_validator.overpass_request import download_data
from osm_ru_nametag_validator.name_checker import name_checker

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

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--refresh', action='store_true',
                      help='принудительно скачать свежие данные')
    mode.add_argument('--local', action='store_true',
                      help='не скачивать, использовать локальный CSV')
    return parser.parse_args()


def main():

    args = parse_args()
    if args.local:
        if not os.path.exists(INPUT):
            sys.exit(f'Ошибка: локальный файл {INPUT} не найден.')

    elif args.refresh or not os.path.exists(INPUT):
        dir_name = os.path.dirname(INPUT)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        download_data(INPUT)

    name_checker(INPUT, DATA_FOLDER)


if __name__ == '__main__':
    main()
