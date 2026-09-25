import os
import sys
import time

import requests

# print() colors
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

API_KEYS = 'API_KEYS.txt'

PUBLIC_OVERPASS_ENDPOINTS = [
    'https://overpass.kumi.systems/api/interpreter',
    'https://overpass.private.coffee/api/interpreter',
    'https://maps.mail.ru/osm/tools/overpass/api/interpreter',
    'https://overpass-api.de/api/interpreter'
]

HEADERS = {'User-Agent': 'lakes-nametag-validator/0.1 (https://github.com/KarelianServal/osm-ru-nametag-validator)'}

QUERY = '''[out:csv(::id, name; true; ",")][timeout:300];
area["ISO3166-1"="RU"]->.russia;
(
  node["natural"="water"]["water"="lake"]["name"](area.russia);
  way["natural"="water"]["water"="lake"]["name"](area.russia);
  relation["natural"="water"]["water"="lake"]["name"](area.russia);
);
out;'''


def download_data(path, retries=3, pause=30):
    print('Загрузка данных с Overpass API (может занять несколько минут)...')

    if os.path.exists(API_KEYS):
        print(f' | {GREEN}Найдены локальные API ключи (API_KEYS.txt){RESET}')

        with open(API_KEYS, 'r', encoding='utf-8') as f:
            LOCAL_OVERPASS_ENDPOINTS = f.read().splitlines()

        for url in LOCAL_OVERPASS_ENDPOINTS:
            print(f' | Пробуем зеркало ({url})...')

            for attempt in range(1, retries + 1):
                try:
                    response = requests.post(
                        url,
                        data={'data': QUERY},
                        headers=HEADERS,
                        timeout=360,
                    )
                    response.raise_for_status()

                    with open(path, 'w', encoding='utf-8', newline='') as f:
                        f.write(response.content.decode('utf-8'))
                        print(f'{GREEN}Сохранено: {path} (зеркало: {url}){RESET}')
                    return

                except requests.RequestException as e:
                    print(f'{RED} | | {url} не ответил: {e}{RESET}')
                    if attempt < retries:
                        print(f'{RED} | | повторная попытка через {pause} с...{RESET}')
                        time.sleep(pause)

        print(f' | Переключаемся на общедоступные API.')

    else:
        print(f'{RED} | Локальные API Overpass (API_KEYS.txt) не найдены.{RESET}')
        print(f'{RED} | Переключаемся на общедоступные API.{RESET}')

    for url in PUBLIC_OVERPASS_ENDPOINTS:
        print(f' | Пробуем зеркало ({url})...')

        for attempt in range(1, retries + 1):
            try:
                response = requests.post(
                    url,
                    data={'data': QUERY},
                    headers=HEADERS,
                    timeout=360,
                )
                response.raise_for_status()

                with open(path, 'w', encoding='utf-8', newline='') as f:
                    f.write(response.content.decode('utf-8'))
                    print(f'{GREEN}Сохранено: {path} (зеркало: {url}){RESET}')
                return

            except requests.RequestException as e:
                print(f'{RED} | | {url} не ответил: {e}{RESET}')
                if attempt < retries:
                    print(f'{RED} | | повторная попытка через {pause} с...{RESET}')
                    time.sleep(pause)
    sys.exit(
        f'{RED}Ошибка: не удалось скачать данные ни с одного зеркала.{RESET}\n'
        f'{RED}Попробуйте позже или запустите с --local, если есть локальный CSV.{RESET}'
    )
