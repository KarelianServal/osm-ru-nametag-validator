import os
import sys

import csv

from .cli_colors import RED, GREEN, RESET
from .overpass_request import overpass_request

PWD_API_KEYS = 'API_KEYS.txt'
PUB_API_KEYS = [
    'https://maps.mail.ru/osm/tools/overpass/api/interpreter',
    'https://overpass-api.de/api/interpreter',
    'https://overpass.private.coffee/api/interpreter',
]


def download_all_regions(API, INPUT):
    ISO_QUERY = '''
    [out:csv("name", "ISO3166-2"; true; ",")][timeout:60];

    area["ISO3166-1"="RU"]->.ru;
    (relation["boundary"="administrative"]["admin_level"="3"](area.ru););
    out;
    '''

    print(' | Находим все RU регионы OSM...')
    regions_query = overpass_request(API, ISO_QUERY)
    regions_query = [row for row in regions_query if row[1]]

    regions_amount = len(regions_query)
    print(f' | Найдено {regions_amount} регионов.')

    data = [['@type', '@id', 'name', 'region', '@lat', '@lon']]

    for i, row in enumerate(regions_query):
        region_name, iso_code = row

        print(f' | ({i+1}/{regions_amount}) Загружаем регион "{region_name}" ({iso_code})...')

        REGION_QUERY = f'''
        [out:csv(::type, ::id, name, ::lat, ::lon; true; ",")][timeout:590];
        area["ISO3166-2"="{iso_code}"]->.region;
        (
        node["natural"="water"]["water"="lake"]["name"](area.region);
        way["natural"="water"]["water"="lake"]["name"](area.region);
        relation["natural"="water"]["water"="lake"]["name"](area.region);
        );
        out center;
        '''
        region_data = overpass_request(API, REGION_QUERY)
        for row in region_data:
            row.insert(3, region_name)
        data += region_data

    with open(INPUT, 'w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerows(data)

    print(f'{GREEN}Сохранено: {INPUT}{RESET}')


def download_data(CLI_API_KEY, INPUT):
    print('Загрузка данных с Overpass API (займет несколько минут):')

    if CLI_API_KEY:
        print(f' | {GREEN}Получен API ключ ({CLI_API_KEY}){RESET}')

        download_all_regions([CLI_API_KEY], INPUT)

    elif os.path.exists(PWD_API_KEYS):
        print(f' | {GREEN}Найдены API ключи (./API_KEYS.txt){RESET}')
        with open(PWD_API_KEYS, 'r', encoding='utf-8') as f:
            OVERPASS_ENDPOINTS = f.read().splitlines()

        download_all_regions(OVERPASS_ENDPOINTS, INPUT)

    elif PUB_API_KEYS:
        print(' | API ключи (./API_KEYS.txt) не найдены')
        print(' | Переключаемся на общедоступные API')
        download_all_regions(PUB_API_KEYS, INPUT)

    else:
        sys.exit(f'{RED}Ошибка: API Overpass (API_KEYS.txt) не найдены.{RESET}')
