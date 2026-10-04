from osm_ru_nametag_validator.name_conditions.rules import (
    name_type
)

valid_substant = [
    'Карачево',
    'Бойково',
    'Щучино',
]
valid_adjf = [
    'Нижнее',
    'Ладожское',
    'Первое',
    'второе',
    'Русское',
]

invalid_adjf = [
    'Айпынгытгын',

    'Камень',
    'Варенье',
    'Портной',
    'Стали',

    'Тангабтэйто',
]

valid_gent = [
    'Стали',
    'Вязок',
    'Бочарова',
    'Левинсон-Лессинга',
    'Мерцбахера',
    'Толмачёва',
    'Усачёва',
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
    for word in valid_substant:
        assert name_type([word]) == 'substant'
    for word in valid_adjf:
        assert name_type([word]) == 'adjf'
    for word in invalid_adjf:
        assert not name_type([word]) == 'adjf'
    for word in valid_gent:
        assert name_type([word]) == 'gent'
    for word in invalid_gent:
        assert not name_type([word]) == 'gent'
