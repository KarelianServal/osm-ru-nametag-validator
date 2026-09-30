from osm_ru_nametag_validator.name_conditions.rules import (
    is_geox_or_adjf,
    is_gent,
)

valid_geox = [
    'Карачево',
    'Бойково',
    'Щучино',
    'Логиярви',
    'Байкал',
    'Сямозеро',
    'ЗАМОЗЕРО',

]
valid_adjf = [
    'Нижнее',
    'Ладожское',
    'Первое',
    'второе',
    'Русское',
]
invalid_adjf = [
    'Камень',
    'Варенье',
    'Портной',
    'Стали',

    'Тангабтэйто',
]

valid_gent = [
    'Стали',
    'Бочарова',
    'Левинсон-Лессинга',
    'Мерцбахера',
    'Толмачёва',
    'Усачёва'
]
invalid_gent = [
    'Тангабтэйто',
    'Тумус-Охто',
    'Валгилампи',
    'Кайдалампи',
    'Малое Кис-Кис',
    'Худагтай',
]
valid_compounds = [
    'Сямозеро',
    'Лемозеро',
    'ЗАМОЗЕРО',
    'Чудо-озеро',
    'Озеро',
    'Озерище',
    'Озерки'
]
invalid_compounds = [
    'Оооооо',
    'озеро',
    'озера',
    'озёра',
    'колесо',
    'река',
    'Логиярви',
    'Байкал',
    'Чудское',
    'Озеозе',
]


def test_rules():
    for word in valid_geox:
        assert is_geox_or_adjf(word) == 'geox'
    for word in valid_adjf:
        assert is_geox_or_adjf(word) == 'adjf'
    for word in invalid_adjf:
        assert not is_geox_or_adjf(word)
    for word in valid_gent:
        assert is_gent(word)
    for word in invalid_gent:
        assert not is_gent(word)
    # for word in valid_compounds:
    #     assert is_compound(word)
    # for word in invalid_compounds:
    #     assert not is_compound(word)
