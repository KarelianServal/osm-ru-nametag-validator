import argparse
import csv
import os
import re
import subprocess
import sys
import time

import requests

INPUT = 'ru-lakes.csv'
SCRIPTS = [
    'name-conditions1.py',
    'name-conditions2.py',
    'name-conditions3.py',
    'name-conditions4.py',
    'name-conditions5.py',
]

OVERPASS_ENDPOINTS = [
    'https://overpass-api.de/api/interpreter',
    'https://overpass.kumi.systems/api/interpreter',
    'https://overpass.private.coffee/api/interpreter',
    'https://overpass.osm.rambler.ru/cgi/interpreter',
]

HEADERS = {'User-Agent': 'lake-name-analyzer/1.0'}

QUERY = '''[out:csv(::id, name; true; ",")][timeout:300];
area["ISO3166-1"="RU"]->.russia;
(
  node["natural"="water"]["water"="lake"]["name"](area.russia);
  way["natural"="water"]["water"="lake"]["name"](area.russia);
  relation["natural"="water"]["water"="lake"]["name"](area.russia);
);
out;'''


def download_data(path, retries=3, pause=30):
    """Скачивает CSV с озёрами России, перебирая зеркала Overpass API."""
    print('Загрузка данных с Overpass API (может занять несколько минут)...')
    for url in OVERPASS_ENDPOINTS:
        for attempt in range(1, retries + 1):
            try:
                response = requests.post(
                    url, data={'data': QUERY}, headers=HEADERS, timeout=360,
                )
                response.raise_for_status()
                # явно декодируем UTF-8, иначе кириллица может испортиться
                with open(path, 'w', encoding='utf-8', newline='') as f:
                    f.write(response.content.decode('utf-8'))
                print(f'Сохранено: {path} (зеркало: {url})')
                return
            except requests.RequestException as e:
                print(f'  {url} не ответил: {e}')
                if attempt < retries:
                    print(f'  повторная попытка через {pause} с...')
                    time.sleep(pause)
    sys.exit(
        'Ошибка: не удалось скачать данные ни с одного зеркала.\n'
        'Попробуйте позже или запустите с --local, если есть локальный CSV.'
    )


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
    parser = argparse.ArgumentParser(description='Анализ имён озёр из OSM на скорую руку. \nhttps://community.openstreetmap.org/t/name/148024',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
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
        download_data(INPUT)

    total = count_total_names(INPUT)
    for i, script in enumerate(SCRIPTS, start=1):
        count = run_script(script)
        pct = round(count / total * 100) if total else 0
        print(f'Условие {i}: {count}/{total} ({pct}%)')


if __name__ == '__main__':
    main()
