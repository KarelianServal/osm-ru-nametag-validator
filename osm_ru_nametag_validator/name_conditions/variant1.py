import re

pattern = re.compile(r'^озеро\b')


def is_variant1(lake_name):
    if lake_name and pattern.match(lake_name):
        return True
    else:
        return False
