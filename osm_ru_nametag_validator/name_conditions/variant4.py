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

TOKEN = re.compile(r'(?<![()\w-])[а-яА-ЯёЁ]+(?:-[а-яА-ЯёЁ0-9]+)*(?![()\w-])')
OZERO = {'озеро', 'озера', 'озёра'}


def matches(name):
    tokens = TOKEN.findall(name.strip())
    if not tokens:
        raise RuntimeError(f'Неверное имя - "{name}"')

    if any(t in OZERO for t in tokens):
        if len(tokens) < 2:
            raise RuntimeError(f'Неверное имя - "{name}"')

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
