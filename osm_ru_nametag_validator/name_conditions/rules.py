import re

from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer()

# pymorphy hallucination workaround:
noun_patterns = {
    # Карело-финский суффикс 'ламби/лампи',
    # означающий 'маленькое лесное озеро'
    'reg_suffix0': re.compile(r'([лЛ]ам[пб]и)'),
    'reg_suffix1': re.compile(r'([яЯ]рви)'),
    # Чукотский суффикс 'гытгын', означающий 'озеро'
    'reg_suffix2': re.compile(r'(ын)$'),
    # Якутия
    'reg_suffix3': re.compile(r'(ин)$'),
    # Ямало-Ненецкий автономный округ
    'reg_suffix4': re.compile(r'(то)$'),

    'reg_suffix5': re.compile(r'(ай)$'),

    'weird_suffix0': re.compile(r'([еЕ]р)$'),
}


def _is_gent(word: MorphAnalyzer.Parse, tokens: list[str]) -> bool:
    # Workaround for "Две Сестры" cases
    if len(tokens) == 1:
        return True
    else:
        second_word = morph.parse(tokens[-2])[0]

        if second_word.tag.POS == 'NUMR':
            return bool(word.tag.number == 'plur')
        else:
            return bool(word.tag.number == second_word.tag.number)


def name_type(tokens: list[str]) -> str:
    word = tokens[-1]

    if morph.word_is_known(word):
        noun_first = False
        parse0 = morph.parse(word)[0]
        if (parse0.tag.case == 'nomn'
                and parse0.tag.POS == 'NOUN'):
            if parse0.score > 0.7:
                return 'noun'
            elif ('Name' in parse0.tag
                    and parse0.tag.number == 'sing'
                    and parse0.score > 0.1):
                return 'noun'
            else:
                noun_first = True

        for p in morph.parse(word):
            if (noun_first
                    and not parse0.tag.gender == 'femn'
                    and parse0.score - p.score > 0.4):
                return 'noun'
            if p.tag.POS == 'ADJS':
                return 'substant'
            if p.tag.POS == 'NOUN' and p.tag.case == 'gent':
                if _is_gent(p, tokens):
                    return 'gent'

    if any(p.search(word) for p in noun_patterns.values()):
        return 'noun'

    for p in morph.parse(word):
        if p.tag.POS == 'NOUN' and 'Geox' in p.tag:
            return 'noun' # substant
        if 'Surn' in p.tag and p.tag.case == 'gent':
            if _is_gent(p, tokens):
                return 'gent'
        if (p.tag.POS == 'ADJF'
                and 'Fixd' not in p.tag):
            return 'adjf'

    return 'noun'
