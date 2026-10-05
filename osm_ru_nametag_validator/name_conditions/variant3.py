'''
Вариант 3: Смешанное наличие слова “озеро” в зависимости от названия озера
(избежание тавтологии)

Есть 4 вида случаев:
1. Cуществительное
   Правильная форма -> 'озеро' до существительного
   Пример: "озеро Байкал"

2. Существительное с 'озеро' внутри имени сообственного
   Правильная форма -> без 'озеро'
   Пример: "Сямозеро"

3. Прилагательное
   Правильная форма -> 'озеро' после прилагательного
   Пример: "Ладожское озеро"

4. Субстантивированное прилагательное-топоним
   Правильная форма -> 'озеро' до существительного
   Пример: "озеро Карачево"
'''

import re
from .rules import name_type

TOKEN = re.compile(r'(?<![()\w-])[а-яА-ЯёЁ]+(?:-[а-яА-ЯёЁ0-9]+)*(?![()\w-])')
OZERO = {'озеро', 'озера', 'озёра'}
COMP = re.compile(r'\b(?!оз[её]р[оа]\b).*[оО][зЗ][еёЕЁ][рР].*\b')


def matches(name):
    tokens = TOKEN.findall(name.strip())
    has_compound = any(COMP.search(t) for t in tokens)

    if any(t in OZERO for t in tokens):
        if len(tokens) < 2:
            raise RuntimeError(f'Неверное имя - {tokens[0]}')
        if has_compound:
            return False

        no_OZERO_tokens = [t for t in tokens if t not in OZERO]

        if tokens[0] in OZERO:
            return name_type(no_OZERO_tokens) != 'adjf'
        if tokens[-1] in OZERO:
            return name_type(no_OZERO_tokens) == 'adjf'

    elif has_compound:
        return True

    return False


def is_variant3(lake_name):
    return lake_name and matches(lake_name)
