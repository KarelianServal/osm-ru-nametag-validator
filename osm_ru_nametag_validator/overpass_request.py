import sys
import time
import threading

import requests

from .cli_colors import RED, RESET
from .statistics import stats
from .api_keys import mask_key

retries = 5  # Times to try to query an API
pause = 20   # Timeout between attempts

HEADERS = {'User-Agent': f'lakes-nametag-validator/{stats["version"]}'
           '(https://github.com/KarelianServal/osm-ru-nametag-validator)'}


def _spin(stop: threading.Event) -> None:
    if not sys.stdout.isatty():
        return

    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    start = time.time()
    while not stop.is_set():
        elapsed = int(time.time() - start)
        sys.stdout.write(f'\r {frames[int(time.time()*10) % len(frames)]}'
                         f'[{elapsed}с] Ожидаем ответа...')
        sys.stdout.flush()
        stop.wait(0.1)


def _clear_spin() -> None:
    sys.stdout.write('\r' + ' ' * 30 + '\r')
    sys.stdout.flush()


def overpass_request(
        OVERPASS_ENDPOINTS: list[str],
        QUERY: str
) -> requests.Response:
    for url in OVERPASS_ENDPOINTS:
        mask = mask_key(url)
        print(f' | Пробуем зеркало ({mask})...')

        for attempt in range(1, retries + 1):
            stop = threading.Event()
            spinner = threading.Thread(target=_spin,
                                       args=(stop,),
                                       daemon=True)
            spinner.start()
            try:
                response = requests.post(
                    url,
                    data={'data': QUERY},
                    headers=HEADERS,
                    timeout=405,
                )
                response.raise_for_status()

                stop.set()
                spinner.join()
                _clear_spin()

                # Check if the response is blank or valid
                text = response.text.strip()
                if len(text) < 20:
                    raise ValueError(f"Слишком короткий ответ: '{text}'")

                if "<!DOCTYPE html>" in text or "<html>" in text.lower():
                    raise ValueError('Сервер вернул HTML страницу ошибки'
                                     'вместо данных')

                time.sleep(4)
                return response

            except requests.RequestException as e:
                stop.set()
                spinner.join()
                _clear_spin()
                print(f' | | {RED}{e}{RESET}')
                if attempt < retries:
                    print(f' | | {RED}Повторная попытка через {pause} с...'
                          '{RESET}')
                    time.sleep(pause)

    sys.exit(
        f'{RED}Ошибка: не удалось скачать данные ни с одного зеркала.{RESET}\n'
        f'{RED}Попробуйте позже или поменяйте API.{RESET}'
    )
