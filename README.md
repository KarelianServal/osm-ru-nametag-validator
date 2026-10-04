
# Table of Contents

1.  [](#org8245724):TOC:
2.  [Установка](#orgb6702b4)
    1.  [pipx](#orga714d76)
    2.  [Ручная установка](#org56f231a)
3.  [Использование](#org99f412b)
    1.  [Overpass API](#orgf2a47e0)
4.  [Данные](#org595d1e7)

Скрипты для анализ имён озёр России из OpenStreetMap: проверка пяти вариантов конвенций именования (наличие и позиция слова «озеро»).

<https://community.openstreetmap.org/t/name/148024>

Соответствие `["natural"="water"]["water"="lake"]["name"]` вариантам на 24.09.2026:

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


<a id="org8245724"></a>

#      :TOC:


<a id="orgb6702b4"></a>

# Установка


<a id="orga714d76"></a>

## pipx

    pipx install git+https://github.com/KarelianServal/osm-ru-nametag-validator


<a id="org56f231a"></a>

## Ручная установка

    git clone https://github.com/KarelianServal/osm-ru-nametag-validator.git \
        && cd osm-ru-nametag-validator
    
    # Создайте виртуальное окружение для пакета (опционально, убирает скрипт из $PATH): 
    python -m venv .venv
    source .venv/bin/activate # или activate.[fish|csh] для fish и csh соответственно
    
    pip install -e .


<a id="org99f412b"></a>

# Использование

    lake-nametag-validator           # Запрос к Overpass API, анализ имен
    lake-nametag-validator --local   # Не делать запрос; использовать локальный ru-lakes.csv
    lake-nametag-validator --refresh # Обновить ru-lakes.csv 
    lake-nametag-validator --api https://... # Использовать свой ключ Overpass

Каждый скрипт variantN.py создаёт variantN.csv
с именами рек, удовлетворяющими условию N.


<a id="orgf2a47e0"></a>

## Overpass API

Скрипт использует публичные API Overpass, [указанные в вики](https://wiki.openstreetmap.org/wiki/Overpass_API#Public_Overpass_API_instances).
Если у вас есть свои API, то их можно использовать, добавив флаг `--api`
или создав файл `API_KEYS.txt` в $PWD:

    https://overpass-api.de/api/interpreter
    https://maps.mail.ru/osm/tools/overpass/api/interpreter
    ...


<a id="org595d1e7"></a>

# Данные

© участники OpenStreetMap, данные распространяются по лицензии ODbL.

