
# Table of Contents

1.  [Установка](#org9799281)
    1.  [pipx](#org84642ad)
    2.  [Ручная установка](#orgc006d80)
2.  [Использование](#org3bfe314)
    1.  [Overpass API](#orgac9d473)
3.  [Данные](#org4ccc47b)

Скрипты для анализ имён озёр России из OpenStreetMap: проверка пяти вариантов конвенций именования (наличие и позиция слова «озеро»).

<https://community.openstreetmap.org/t/name/148024>

Соответствие `["natural"="water"]["water"="lake"]["name"]` [вариантам](./VARIANTS.md) на 06.10.2026:

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-left">Исключения</td>
<td class="org-left">1663/39712</td>
<td class="org-right">4%</td>
</tr>

<tr>
<td class="org-left">Вариант 1</td>
<td class="org-left">11535/38049</td>
<td class="org-right">30%</td>
</tr>

<tr>
<td class="org-left">Вариант 2</td>
<td class="org-left">9241/38049</td>
<td class="org-right">24%</td>
</tr>

<tr>
<td class="org-left">Вариант 3</td>
<td class="org-left">10970/38049</td>
<td class="org-right">29%</td>
</tr>

<tr>
<td class="org-left">Вариант 4</td>
<td class="org-left">18083/38049</td>
<td class="org-right">48%</td>
</tr>

<tr>
<td class="org-left">Вариант 5</td>
<td class="org-left">23835/38049</td>
<td class="org-right">63%</td>
</tr>
</tbody>
</table>


<a id="org9799281"></a>

# Установка


<a id="org84642ad"></a>

## pipx

    pipx install git+https://github.com/KarelianServal/osm-ru-nametag-validator


<a id="orgc006d80"></a>

## Ручная установка

    git clone https://github.com/KarelianServal/osm-ru-nametag-validator.git \
        && cd osm-ru-nametag-validator
    
    # Создайте виртуальное окружение для пакета (опционально, убирает скрипт из $PATH): 
    python -m venv .venv
    source .venv/bin/activate # или activate.[fish|csh] для fish и csh соответственно
    
    pip install -e .


<a id="org3bfe314"></a>

# Использование

    lake-nametag-validator           # Запрос к Overpass API, анализ имен
    lake-nametag-validator --local   # Не делать запрос; использовать локальный ru-lakes.csv
    lake-nametag-validator --refresh # Обновить ru-lakes.csv 
    lake-nametag-validator --api https://... # Использовать свой ключ Overpass

Каждый скрипт variantN.py создаёт variantN.csv
с именами рек, удовлетворяющими условию N.


<a id="orgac9d473"></a>

## Overpass API

Скрипт использует публичные API Overpass, [указанные в вики](https://wiki.openstreetmap.org/wiki/Overpass_API#Public_Overpass_API_instances).
Если у вас есть свои API, то их можно использовать, добавив флаг `--api`
или создав файл `API_KEYS.txt` в $PWD:

    https://overpass-api.de/api/interpreter
    https://maps.mail.ru/osm/tools/overpass/api/interpreter
    ...


<a id="org4ccc47b"></a>

# Данные

© участники OpenStreetMap, данные распространяются по лицензии ODbL.

