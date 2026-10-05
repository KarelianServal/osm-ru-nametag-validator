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
from .rules import name_type

TOKEN = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)?")
OZERO = {'озеро', 'озера', 'озёра'}
NUM = re.compile(r"[0-9]+-\w+")  # 1-й, 2-ая


def matches(name):
    tokens = [t for t in TOKEN.findall(name.strip()) if not NUM.search(t)]

    if any(t in OZERO for t in tokens):
        if len(tokens) < 2:
            raise RuntimeError(f'Неверное имя - "{tokens[0]}"')

        no_OZERO_tokens = [t for t in tokens if t not in OZERO]

        if tokens[0] in OZERO:
            return name_type(no_OZERO_tokens) == 'gent'
        if tokens[-1] in OZERO:
            return name_type(no_OZERO_tokens) == 'adjf'

    else:
        return name_type(tokens) not in ('adjf', 'gent')

    return False


def is_variant4(lake_name):
    return lake_name and matches(lake_name)
