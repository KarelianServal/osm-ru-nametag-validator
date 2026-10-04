'''
Вариант 2: Свободное обязательное наличие слова “озеро” в зависимости от
имени сообственного

Есть 3 вида случаев:
1. Cуществительное
   Правильная форма -> 'озеро' до существительного
   Пример: "озеро Байкал"

2. Прилагательное
   Правильная форма -> 'озеро' после прилагательного
   Пример: "Ладожское озеро"

3. Субстантивированное прилагательное-топоним
   Правильная форма -> 'озеро' до существительного
   Пример: "озеро Карачево"
'''

import re
from .rules import name_type

TOKEN = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)?")
OZERO = {'озеро', 'озера', 'озёра'}


def matches(name):
    tokens = TOKEN.findall(name.strip())

    if any(t in OZERO for t in tokens):
        if len(tokens) < 2:
            raise RuntimeError(f'Неверное имя - {tokens[0]}')

        if tokens[0] in OZERO:
            if name_type(tokens[-1]) != 'adjf':
                return True

        if tokens[-1] in OZERO:
            if name_type(tokens[-2]) == 'adjf':
                return True

    return False


def is_variant2(lake_name):
    return lake_name and matches(lake_name)
