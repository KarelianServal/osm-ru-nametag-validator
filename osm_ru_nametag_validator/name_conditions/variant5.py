'''
Вариант 5: Отсутствие “озеро” в имени озера.

Пример: "озеро Байкал"
'''

import re

pattern = re.compile(r'^.*\b(озеро|озера|озёра)\b.*$')


def is_variant5(lake_name):
    return lake_name and not pattern.match(lake_name)
