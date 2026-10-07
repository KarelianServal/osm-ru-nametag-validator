import os
import sys

from .cli_colors import GREEN, RED, RESET

PWD_API_KEYS = 'API_KEYS.txt'

PUB_API_KEYS = [
    'https://maps.mail.ru/osm/tools/overpass/api/interpreter',
    'https://overpass-api.de/api/interpreter',
    'https://overpass.private.coffee/api/interpreter',
]


def get_api_keys(CLI_API_KEY):
    if CLI_API_KEY:
        print(f'{GREEN}Получен API ключ ({CLI_API_KEY}){RESET}')
        return CLI_API_KEY

    elif os.path.exists(PWD_API_KEYS):
        print(f'{GREEN}Найдены API ключи (./API_KEYS.txt){RESET}')
        with open(PWD_API_KEYS, 'r', encoding='utf-8') as f:
            return f.read().splitlines()

    elif PUB_API_KEYS:
        print('API ключи (./API_KEYS.txt) не найдены')
        print('Переключаемся на общедоступные API')
        return PUB_API_KEYS

    else:
        sys.exit(f'{RED}Ошибка: API Overpass (API_KEYS.txt) не найдены.{RESET}')
