'''
Вариант 4: Наличие слова “озеро” только если оно является неотъемлемой частью
названия,в соответствии с wiki/RU:Названия

Есть 4 вида случаев:
1. Cуществительное
   Правильная форма -> без 'озеро'
   Пример: "Байкал"

2. Существительное в родительном падаже
   Правильная форма -> 'озеро' до существительного
   Пример: "озеро Бочарова"

3. Прилагательное
   Правильная форма -> 'озеро' после прилагательного
   Пример: "Ладожское озеро"

4. Субстантивированное прилагательное-топоним
   Правильная форма -> без 'озеро'
   Пример: "Карачево"
'''

import re
from pymorphy3 import MorphAnalyzer

from .rules import name_type

morph = MorphAnalyzer()
TOKEN = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)?")
OZERO = {'озеро', 'озера', 'озёра'}


def matches(name):
    tokens = TOKEN.findall(name.strip())

    if any(t in OZERO for t in tokens):
        if len(tokens) < 2:
            raise RuntimeError(f'Неверное имя - "{tokens[0]}"')

        if tokens[0] in OZERO:
            if name_type(tokens[-1]) == 'gent':
                return True

        if tokens[-1] in OZERO:
            if name_type(tokens[-2]) == 'adjf':
                return True

    else:
        if name_type(tokens[-1]) not in ('adjf', 'gent'):
            return True

    return False


def is_variant4(lake_name):
    return lake_name and matches(lake_name)
