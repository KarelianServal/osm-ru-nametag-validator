import re

# Edge-cases
unique = {
    ('relation', "2650915"),   # Сухое Озеро
}


patterns = {
    'whitelist_invalid_chars': re.compile(r'[^а-яА-ЯёЁ()\-\\\s]'),

    'double_spaces': re.compile(r'\s{2,}'),

    'hyphen': re.compile(r'\b(озеро|озера|озёра)[-–—]\b'),

    'OzErO': re.compile(r'\b(?!озеро|озера|озёра)[оО][зЗ][еЕёЁ][рР][оОаА]\b'),

    'ozer': re.compile(r'\b(?!озеро|озера|озёра)[оО][зЗ][еЕёЁ][рР][оОаА]*\b'),
    'ozeo': re.compile(r'\b(?!озеро|озера|озёра)[оО][зЗ][еЕёЁ][рР]*[оОаА]\b'),
    'ozro': re.compile(r'\b(?!озеро|озера|озёра)[оО][зЗ][еЕёЁ]*[рР][оОаА]\b'),
    'oero': re.compile(r'\b(?!озеро|озера|озёра)[оО][зЗ]*[еЕёЁ][рР][оОаА]\b'),
    'zero': re.compile(r'\b(?!озеро|озера|озёра)[оО]*[зЗ][еЕёЁ][рР][оОаА]\b'),

    'only_ozero_no_name': re.compile(r'^[оО][зЗ][еЕёЁ][рР][оОаА]$'),
}


def is_exception(osm_type, osm_id, name):
    if (osm_type, osm_id) not in unique:
        return any(p.search(name) for p in patterns.values())
