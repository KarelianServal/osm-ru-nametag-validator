import sys
import time
from io import StringIO

import requests
import csv

from .cli_colors import RED, RESET

retries = 5  # Times to try to query an API
pause = 15   # Timeout between attempts

HEADERS = {'User-Agent': 'lakes-nametag-validator/0.1.4 (https://github.com/KarelianServal/osm-ru-nametag-validator)'}


def overpass_request(OVERPASS_ENDPOINTS,  QUERY):
    for url in OVERPASS_ENDPOINTS:
        print(f' | | Пробуем зеркало ({url})...')

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

                content = list(csv.reader(StringIO(content)))[1:]

                time.sleep(4)
                return content

            except requests.RequestException as e:
                print(f' | | | {RED}{url} не ответил: {e}{RESET}')
                if attempt < retries:
                    print(f' | | | {RED}повторная попытка через {pause} с...{RESET}')
                    time.sleep(pause)

    sys.exit(
        f'{RED}Ошибка: не удалось скачать данные ни с одного зеркала.{RESET}\n'
        f'{RED}Попробуйте позже или поменяйте API.{RESET}'
    )
