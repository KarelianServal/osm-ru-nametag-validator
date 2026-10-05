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

TOKEN = re.compile(r'(?<![()\w-])[а-яА-ЯёЁ]+(?:-[а-яА-ЯёЁ0-9]+)*(?![()\w-])')
OZERO = {'озеро', 'озера', 'озёра'}


def matches(name):
    tokens = TOKEN.findall(name.strip())

    if any(t in OZERO for t in tokens):
        if len(tokens) < 2:
            raise RuntimeError(f'Неверное имя - {name}')

        no_OZERO_tokens = [t for t in tokens if t not in OZERO]

        if tokens[0] in OZERO:
            return name_type(no_OZERO_tokens) != 'adjf'
        if tokens[-1] in OZERO:
            return name_type(no_OZERO_tokens) == 'adjf'

    return False


def is_variant2(lake_name):
    return lake_name and matches(lake_name)
