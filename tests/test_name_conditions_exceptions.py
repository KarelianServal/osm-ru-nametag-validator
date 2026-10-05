from osm_ru_nametag_validator.name_conditions.exceptions import is_exception

valid_exceptions = [
    '',
    '   ',

    '.',
    'Ozero Logiyarvi',
    'озеро №2',

    'Куехтанар 3',
    'озеро 13',
    'озеро Арылах 1',
    '1239',
    '4',

    'озеро  Байкал',

    'озеро-Байкал',
    'озеро—Байкал',

    '-Байкал',
    'Байкал-',

    'Байкал(озеро)',

    'ОзЕрО Байкал',

    'озер Байкал',
    'озео Байкал',
    'озро Байкал',
    'оеро Байкал',
    'зеро Байкал',

    'озеро',
    'озера',
    'озёра',

    'озеро 1-е',
    '1-е озеро',
    'озеро 53-е',
    'озеро 1',

    'озеро байкал',
]

non_valid_exceptions = [
    'Ивановское 2-ое',
    'Стружец 1-ое',
    'Гагарье 1-е',
    'Дуроевское 1-е',
    'Итикан 1-й',
    'Дякян 1-й',
    'Танатар 3-й',
    'Пай 9-й',
    'Пельга 3-я',
    '1-е Джангоршайское',
    '1-е Окуневое',
    'Мунду-Кюель 2-е',
    'Чвор 3-й',
]


def test_is_exception():
    for name in valid_exceptions:
        assert is_exception(0, 0, name)
    for name in non_valid_exceptions:
        assert not is_exception(0, 0, name)

    assert is_exception(0, 0, '149TEst.$%#№')
    assert not is_exception('relation', '2650915', '149TEst.$%#№')
