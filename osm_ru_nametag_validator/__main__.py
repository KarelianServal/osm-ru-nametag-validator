import argparse
import csv
import os
import re
import subprocess
import sys

from osm_ru_nametag_validator.overpass_request import download_data

INPUT = 'out/ru-lakes.csv'
SCRIPTS = [
    'osm_ru_nametag_validator/conditions_checker/variant1.py',
    'osm_ru_nametag_validator/conditions_checker/variant2.py',
    'osm_ru_nametag_validator/conditions_checker/variant3.py',
    'osm_ru_nametag_validator/conditions_checker/variant4.py',
    'osm_ru_nametag_validator/conditions_checker/variant5.py',
]


def count_total_names(path):
    """Количество строк с непустым именем в исходном CSV."""
    with open(path, encoding='utf-8-sig') as f:
        return sum(
            1 for row in csv.DictReader(f)
            if (row.get('name') or '').strip()
        )


def run_script(script):
    """Запускает скрипт и извлекает посчитанное им число из его вывода."""
    proc = subprocess.run(
        [sys.executable, script],
        check=True, capture_output=True, text=True,
    )
    numbers = re.findall(r'\d+', proc.stdout)
    return int(numbers[-1])


def parse_args():
    parser = argparse.ArgumentParser(
                 description='\
  Анализ тега [name=] озёр из OSM.\n\
  https://community.openstreetmap.org/t/name/148024',
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

    total = count_total_names(INPUT)
    for i, script in enumerate(SCRIPTS, start=1):
        count = run_script(script)
        pct = round(count / total * 100) if total else 0
        print(f'Условие {i}: {count}/{total} ({pct}%)')


if __name__ == '__main__':
    main()
