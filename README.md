
# Table of Contents

1.  [Установка](#orge230b81)
    1.  [pipx](#org23d40e6)
    2.  [Ручная установка](#org81f3470)
2.  [Использование](#orgdec00fc)
    1.  [Overpass API](#org341ae82)
3.  [Данные](#org10227c3)

Скрипты для анализ имён озёр России из OpenStreetMap: проверка пяти вариантов конвенций именования (наличие и позиция слова «озеро»).

<https://community.openstreetmap.org/t/name/148024>

Соответствие `["natural"="water"]["water"="lake"]["name"]` [вариантам](./VARIANTS.md) на 05.10.2026:

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-left">Исключения</td>
<td class="org-left">1834/39715</td>
<td class="org-right">5%</td>
</tr>

<tr>
<td class="org-left">Вариант 1</td>
<td class="org-left">11469/37881</td>
<td class="org-right">30%</td>
</tr>

<tr>
<td class="org-left">Вариант 2</td>
<td class="org-left">9199/37881</td>
<td class="org-right">24%</td>
</tr>

<tr>
<td class="org-left">Вариант 3</td>
<td class="org-left">10928/37881</td>
<td class="org-right">29%</td>
</tr>

<tr>
<td class="org-left">Вариант 4</td>
<td class="org-left">17979/37881</td>
<td class="org-right">47%</td>
</tr>

<tr>
<td class="org-left">Вариант 5</td>
<td class="org-left">23749/37881</td>
<td class="org-right">63%</td>
</tr>
</tbody>
</table>


<a id="orge230b81"></a>

# Установка


<a id="org23d40e6"></a>

## pipx

    pipx install git+https://github.com/KarelianServal/osm-ru-nametag-validator


<a id="org81f3470"></a>

## Ручная установка

    git clone https://github.com/KarelianServal/osm-ru-nametag-validator.git \
        && cd osm-ru-nametag-validator
    
    # Создайте виртуальное окружение для пакета (опционально, убирает скрипт из $PATH): 
    python -m venv .venv
    source .venv/bin/activate # или activate.[fish|csh] для fish и csh соответственно
    
    pip install -e .


<a id="orgdec00fc"></a>

# Использование

    lake-nametag-validator           # Запрос к Overpass API, анализ имен
    lake-nametag-validator --local   # Не делать запрос; использовать локальный ru-lakes.csv
    lake-nametag-validator --refresh # Обновить ru-lakes.csv 
    lake-nametag-validator --api https://... # Использовать свой ключ Overpass

Каждый скрипт variantN.py создаёт variantN.csv
с именами рек, удовлетворяющими условию N.


<a id="org341ae82"></a>

## Overpass API

Скрипт использует публичные API Overpass, [указанные в вики](https://wiki.openstreetmap.org/wiki/Overpass_API#Public_Overpass_API_instances).
Если у вас есть свои API, то их можно использовать, добавив флаг `--api`
или создав файл `API_KEYS.txt` в $PWD:

    https://overpass-api.de/api/interpreter
    https://maps.mail.ru/osm/tools/overpass/api/interpreter
    ...


<a id="org10227c3"></a>

# Данные

© участники OpenStreetMap, данные распространяются по лицензии ODbL.

