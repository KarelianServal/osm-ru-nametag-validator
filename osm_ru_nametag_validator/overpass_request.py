import sys
import time

import requests

from .cli_colors import RED, RESET

retries = 5  # Times to try to query an API
pause = 15   # Timeout between attempts

HEADERS = {'User-Agent': 'lakes-nametag-validator/0.1.4 (https://github.com/KarelianServal/osm-ru-nametag-validator)'}


def overpass_request(OVERPASS_ENDPOINTS,  QUERY):
    for url in OVERPASS_ENDPOINTS:
        print(f' | Пробуем зеркало ({url})...')

        for attempt in range(1, retries + 1):
            try:
                response = requests.post(
                    url,
                    data={'data': QUERY},
                    headers=HEADERS,
                    timeout=1600,
                )
                response.raise_for_status()

                # Check if the response is blank or valid
                text = response.text.strip()
                if len(text) < 20:
                    raise ValueError(f"Слишком короткий ответ: '{text}'")

                if "<!DOCTYPE html>" in text or "<html>" in text.lower():
                    raise ValueError("Сервер вернул HTML страницу ошибки вместо данных")

                time.sleep(4)
                return response

            except requests.RequestException as e:
                print(f' | | {RED}{url} не ответил: {e}{RESET}')
                if attempt < retries:
                    print(f' | | {RED}повторная попытка через {pause} с...{RESET}')
                    time.sleep(pause)

    sys.exit(
        f'{RED}Ошибка: не удалось скачать данные ни с одного зеркала.{RESET}\n'
        f'{RED}Попробуйте позже или поменяйте API.{RESET}'
    )
