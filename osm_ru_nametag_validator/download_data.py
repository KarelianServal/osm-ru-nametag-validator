import csv
from io import StringIO

from .cli_colors import RED, GREEN, RESET
from .overpass_request import overpass_request

LAKES_QUERY = '''
[out:csv(::type, ::id, name, ::lat, ::lon; true; ",")][timeout:590];
area["ISO3166-1"="RU"]->.ru;
(
node["natural"="water"]["water"="lake"]["name"](area.ru);
way["natural"="water"]["water"="lake"]["name"](area.ru);
relation["natural"="water"]["water"="lake"]["name"](area.ru);
);
out center;
'''


def download_lakes(API, LAKES_DATA):
    print('Загрузка озер с Overpass API (займет несколько минут):')
    lakes_data = overpass_request(API, LAKES_QUERY)
    lakes_data = lakes_data.content.decode('utf-8')
    lakes_data = list(csv.reader(StringIO(lakes_data)))[1:]

    lakes_data = [['@type', '@id', 'name',
                   '@lat', '@lon']] + lakes_data

    with open(LAKES_DATA, 'w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerows(lakes_data)

    print(f'{GREEN}Сохранено: {LAKES_DATA}{RESET}')
