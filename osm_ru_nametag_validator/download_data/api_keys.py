import os
import sys
import re

from ..constants.cli_colors import GREEN, RED, RESET

PWD_API_KEYS = 'API_KEYS.txt'

PUB_API_KEYS = [
    'https://maps.mail.ru/osm/tools/overpass/api/interpreter',
    'https://overpass-api.de/api/interpreter',
    'https://overpass.private.coffee/api/interpreter',
]

MASK_RE = re.compile(
    r"(?:(?<=://)[^/?#]*)"
    r"|(?<![A-Za-z0-9_-])"
    r"(?:osm|tools|overpass|api/interpreter)"
    r"(?![A-Za-z0-9_-])"
    r"|([A-Za-z0-9_-]{7,})"
)


def _short(s: str) -> str:
    return s[:4] + "…" if len(s) > 8 else "***"


def mask_key(key: str) -> str:
    return MASK_RE.sub(
        lambda m: _short(m.group(1)) if m.group(1) is not None else m.group(0),
        key
    )


def get_api_keys(CLI_API_KEY: str) -> list[str]:
    if CLI_API_KEY:
        mask = mask_key(CLI_API_KEY)
        print(f'{GREEN}Получен API ключ ({mask}){RESET}')
        return [CLI_API_KEY]

    elif os.path.exists(PWD_API_KEYS):
        print(f'{GREEN}Найдены API ключи (./API_KEYS.txt){RESET}')
        with open(PWD_API_KEYS, 'r', encoding='utf-8') as f:
            return f.read().splitlines()

    elif PUB_API_KEYS:
        print('API ключи (./API_KEYS.txt) не найдены')
        print('Переключаемся на общедоступные API')
        return PUB_API_KEYS

    else:
        sys.exit(f'{RED}'
                 'Ошибка: API Overpass (API_KEYS.txt) не найдены.'
                 '{RESET}')
