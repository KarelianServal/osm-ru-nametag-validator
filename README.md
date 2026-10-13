
# Table of Contents

1.  [Установка](#org60e3d59)
    1.  [pipx](#org8631863)
    2.  [Ручная установка](#org34e414d)
2.  [Использование](#orgaba5fbf)
    1.  [Overpass API](#org31a380a)
3.  [Лицензирование](#org6f142d4)

Скрипты для анализ имён озёр России из OpenStreetMap: проверка пяти вариантов конвенций именования (наличие и позиция слова «озеро»).

<https://community.openstreetmap.org/t/name/148024>


<a id="org60e3d59"></a>

# Установка


<a id="org8631863"></a>

## pipx

    pipx install git+https://github.com/KarelianServal/osm-ru-nametag-validator


<a id="org34e414d"></a>

## Ручная установка

    git clone https://github.com/KarelianServal/osm-ru-nametag-validator.git \
        && cd osm-ru-nametag-validator
    
    # Создайте виртуальное окружение для пакета (опционально, убирает скрипт из $PATH): 
    python -m venv .venv
    source .venv/bin/activate # или activate.[fish|csh] для fish и csh соответственно
    
    pip install -e .


<a id="orgaba5fbf"></a>

# Использование

    lakes-nametag-validator                   # Запрос к Overpass API, анализ имен
    lakes-nametag-validator --api <API>       # Использовать свой ключ Overpass
    lakes-nametag-validator --local           # использовать локальный ru-lakes.csv
    lakes-nametag-validator --refresh         # Обновить ru-lakes.csv 
    lakes-nametag-validator --refresh-regions # Обновить ru-regions.geojson
    lakes-nametag-validator --json            #  выводить озера в формате .json
    lakes-nametag-validator --out-dir <DIR>   # Выбрать директорию для вывода

Каждый скрипт `variant<i>.py` создаёт фаил `variant<i>/<регион>.csv`
с именами рек региона, удовлетворяющими условию N.


<a id="org31a380a"></a>

## Overpass API

Скрипт использует публичные API Overpass, [указанные в вики](https://wiki.openstreetmap.org/wiki/Overpass_API#Public_Overpass_API_instances).
Если у вас есть свои API, то их можно использовать, добавив флаг `--api`
или создав файл `API_KEYS.txt` в $PWD:

    https://overpass-api.de/api/interpreter
    https://maps.mail.ru/osm/tools/overpass/api/interpreter
    ...

Если у вас есть свои данные рек (`ru-lakes.csv`) или границ регионов(`ru-regions.geojson`), поместите их в директорию `data/`

Важно: таблица (`ru-lakes.csv`) должна выглядеть таким образом:

    @type;@id;name;region;@lat;@lon
    way;132546383;озеро Сосновское;Алтайский край;53.5314321;83.6942961
    relation;6587825;Чистые озёра;Алтайский край;53.3235729;83.53153
    relation;545229;озеро Никольское;Вологодская область;59.83778;38.7723872
    ...


<a id="org6f142d4"></a>

# Лицензирование
- Код проекта распространяется под [GPL-3.0](./LICENSE)
- Шрифты, использованные в ассетах, распространяются под [OFL 1.1](./zine/assets/fonts/OFL.txt):
  - "PT Sans": Copyright (c) 2010, [ParaType Ltd.](http://www.paratype.com/public)
  - "PT Serif": Copyright (c) 2010, [ParaType Ltd.](http://www.paratype.com/public)
  - "Iosevka": Copyright (c) 2015-2026, Renzhi Li (aka. Belleve Invis,
belleve@typeof.net)
- Данные карты распространяются по [лицензии ODbL](https://www.openstreetmap.org/copyright):
  - Copyright (c) OpenStreetMap contributors

