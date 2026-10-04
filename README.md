
# Table of Contents

1.  [Установка](#org3a339ac)
    1.  [pipx](#orgc43e8c4)
    2.  [Ручная установка](#orgc7af24e)
2.  [Использование](#orge63e7a2)
    1.  [Overpass API](#orgec869d5)
3.  [Данные](#org4e364bb)

Скрипты для анализ имён озёр России из OpenStreetMap: проверка пяти вариантов конвенций именования (наличие и позиция слова «озеро»).

<https://community.openstreetmap.org/t/name/148024>

Соответствие `["natural"="water"]["water"="lake"]["name"]` [вариантам](./VARIANTS.md)  на 05.10.2026:

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-left">Исключения</td>
<td class="org-left">1593/39713</td>
<td class="org-right">4%</td>
</tr>

<tr>
<td class="org-left">Вариант 1</td>
<td class="org-left">11509/38120</td>
<td class="org-right">30%</td>
</tr>

<tr>
<td class="org-left">Вариант 2</td>
<td class="org-left">9209/38120</td>
<td class="org-right">24%</td>
</tr>

<tr>
<td class="org-left">Вариант 3</td>
<td class="org-left">10939/38120</td>
<td class="org-right">29%</td>
</tr>

<tr>
<td class="org-left">Вариант 4</td>
<td class="org-left">18125/38120</td>
<td class="org-right">48%</td>
</tr>

<tr>
<td class="org-left">Вариант 5</td>
<td class="org-left">23935/38120</td>
<td class="org-right">63%</td>
</tr>
</tbody>
</table>


<a id="org3a339ac"></a>

# Установка


<a id="orgc43e8c4"></a>

## pipx

    pipx install git+https://github.com/KarelianServal/osm-ru-nametag-validator


<a id="orgc7af24e"></a>

## Ручная установка

    git clone https://github.com/KarelianServal/osm-ru-nametag-validator.git \
        && cd osm-ru-nametag-validator
    
    # Создайте виртуальное окружение для пакета (опционально, убирает скрипт из $PATH): 
    python -m venv .venv
    source .venv/bin/activate # или activate.[fish|csh] для fish и csh соответственно
    
    pip install -e .


<a id="orge63e7a2"></a>

# Использование

    lake-nametag-validator           # Запрос к Overpass API, анализ имен
    lake-nametag-validator --local   # Не делать запрос; использовать локальный ru-lakes.csv
    lake-nametag-validator --refresh # Обновить ru-lakes.csv 
    lake-nametag-validator --api https://... # Использовать свой ключ Overpass

Каждый скрипт variantN.py создаёт variantN.csv
с именами рек, удовлетворяющими условию N.


<a id="orgec869d5"></a>

## Overpass API

Скрипт использует публичные API Overpass, [указанные в вики](https://wiki.openstreetmap.org/wiki/Overpass_API#Public_Overpass_API_instances).
Если у вас есть свои API, то их можно использовать, добавив флаг `--api`
или создав файл `API_KEYS.txt` в $PWD:

    https://overpass-api.de/api/interpreter
    https://maps.mail.ru/osm/tools/overpass/api/interpreter
    ...


<a id="org4e364bb"></a>

# Данные

© участники OpenStreetMap, данные распространяются по лицензии ODbL.

