import os
import sys
import time

import requests

from .cli_colors import RED, GREEN, RESET

PWD_API_KEYS = 'API_KEYS.txt'
PUB_API_KEYS = [
    'https://overpass.private.coffee/api/interpreter',
    'https://maps.mail.ru/osm/tools/overpass/api/interpreter',
    'https://overpass-api.de/api/interpreter'
]

retries = 3  # Times to try to query an API
pause = 20   # Timeout between attempts

HEADERS = {'User-Agent': 'lakes-nametag-validator/0.1.0 (https://github.com/KarelianServal/osm-ru-nametag-validator)'}

QUERY = '''[out:csv(::id, name; true; ",")][timeout:590];
area["ISO3166-1"="RU"]->.russia;
(
  node["natural"="water"]["water"="lake"]["name"](area.russia);
  way["natural"="water"]["water"="lake"]["name"](area.russia);
  relation["natural"="water"]["water"="lake"]["name"](area.russia);
);
out;'''


def overpass_request(OVERPASS_ENDPOINTS, INPUT):
    for url in OVERPASS_ENDPOINTS:
        print(f' | Пробуем зеркало ({url})...')

        for attempt in range(1, retries + 1):
            try:
                response = requests.post(
                    url,
                    data={'data': QUERY},
                    headers=HEADERS,
                    timeout=600,
                )
                response.raise_for_status()

                content = response.content.decode('utf-8')
                # Check if the response is blank or valid
                if len(content.strip().splitlines()) <= 1:
                    raise ValueError("Сервер вернул пустые данные")

                with open(INPUT, 'w', encoding='utf-8', newline='') as f:
                    f.write(content)
                    print(f'{GREEN}Сохранено: {INPUT} (зеркало: {url}){RESET}')
                return

            except requests.RequestException as e:
                print(f' | | {RED}{url} не ответил: {e}{RESET}')
                if attempt < retries:
                    print(f' | | {RED}повторная попытка через {pause} с...{RESET}')
                    time.sleep(pause)

    sys.exit(
        f'{RED}Ошибка: не удалось скачать данные ни с одного зеркала.{RESET}\n'
        f'{RED}Попробуйте позже или поменяйте API.{RESET}'
    )


def download_data(CLI_API_KEY, INPUT):
    print('Загрузка данных с Overpass API (может занять несколько минут)...')

    if CLI_API_KEY:
        print(f' | {GREEN}Получен API ключ ({CLI_API_KEY}){RESET}')

        overpass_request([CLI_API_KEY], INPUT)

    elif os.path.exists(PWD_API_KEYS):
        print(f' | {GREEN}Найдены API ключи (./API_KEYS.txt){RESET}')
        with open(PWD_API_KEYS, 'r', encoding='utf-8') as f:
            OVERPASS_ENDPOINTS = f.read().splitlines()

        overpass_request(OVERPASS_ENDPOINTS, INPUT)

    elif PUB_API_KEYS:
        print(' | API ключи (./API_KEYS.txt) не найдены')
        print(' | Переключаемся на общедоступные API')
        overpass_request(PUB_API_KEYS, INPUT)

    else:
        sys.exit(f'{RED}Ошибка: API Overpass (API_KEYS.txt) не найдены.{RESET}')
