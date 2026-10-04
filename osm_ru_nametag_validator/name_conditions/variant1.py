'''
Вариант 1: Строгое наличие слова “озеро” в начале.

Пример: "озеро Байкал"
'''

import re

pattern = re.compile(r'^(озеро|озера|озёра)\b')


def is_variant1(lake_name):
    return lake_name and pattern.match(lake_name)
