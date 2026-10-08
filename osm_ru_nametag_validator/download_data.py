from io import StringIO
from pandas import read_csv

import geopandas

from shapely.errors import GEOSException
from shapely.geometry import LineString, mapping
from shapely.ops import polygonize, unary_union


from .cli_colors import RED, GREEN, RESET
from .overpass_request import overpass_request
from .calculate_regions import attach_regions

REGIONS_QUERY = '''
[out:json][timeout:300];
area["ISO3166-1"="RU"]->.ru;
relation["boundary"="administrative"]["admin_level"="4"](area.ru);
out geom qt;
'''

LAKES_QUERY = '''
[out:csv(::type, ::id, name, ::lat, ::lon; true; ";")][timeout:400];
area["ISO3166-1"="RU"]->.ru;
(
node["natural"="water"]["water"="lake"]["name"](area.ru);
way["natural"="water"]["water"="lake"]["name"](area.ru);
relation["natural"="water"]["water"="lake"]["name"](area.ru);
);
out center;
'''


def _relation_to_feature(rel):
    rel_id = rel.get("id", "?")

    def skip(reason):
        print(f"{RED}[SKIP] Relation {rel_id}: {reason}{RESET}")
        return None

    outer, inner = [], []

    for member in rel.get("members", []):
        if member.get("type") != "way":
            continue
        geom = member.get("geometry") or []
        if len(geom) < 2:
            continue

        coords = [(p["lon"], p["lat"]) for p in geom]
        line = LineString(coords)

        role = member.get("role", "")
        if role == "inner":
            inner.append(line)
        else:
            outer.append(line)

    if not outer:
        return skip("нет внешних линий")

    outer_polys = list(polygonize(unary_union(outer))) if outer else []

    if not outer_polys:
        return skip(f"0 полигонов из {len(outer)} линий")

    try:
        geometry = unary_union(outer_polys)
        inner_polys = list(polygonize(unary_union(inner))) if inner else []

        if inner and not inner_polys:
            print(f"[WARN] Relation {rel_id}: внутренние линии не замкнулись")
        if inner_polys:
            geometry = geometry.difference(unary_union(inner_polys))
    except GEOSException as e:
        return skip(f"ошибка GEOS: {e}")

    if geometry.is_empty:
        return skip("итоговая геометрия пуста (difference убрал полигоны?)")

    if geometry.geom_type not in ("Polygon", "MultiPolygon"):
        polys = [g for g in getattr(geometry, "geoms", [])
                 if g.geom_type in ("Polygon", "MultiPolygon")]

        if not polys:
            return skip(f"тип {geometry.geom_type}")
        geometry = unary_union(polys)

    return {
        "type": "Feature",
        "properties": rel.get("tags", {}),
        "geometry": mapping(geometry),
    }


def download_regions(API, REGIONS_DATA):
    print('Загрузка регионов с Overpass (может занять несколько минут)...')

    regions_data = overpass_request(API, REGIONS_QUERY).json()

    elements = regions_data.get("elements", [])
    if not elements:
        raise RuntimeError("Overpass вернул пустой ответ")

    has_geometry = any(
        "geometry" in m
        for el in elements
        if el.get("type") == "relation"
        for m in el.get("members", [])
    )

    if not has_geometry:
        raise RuntimeError(
            "Overpass не вернул геометрию для отношений. "
            "Сервер перегружен или таймаут слишком мал. "
            "Попробуйте позже или используйте готовый GeoJSON."
        )

    features = [
        f for el in elements
        if el.get("type") == "relation"
        for f in [_relation_to_feature(el)] if f
    ]

    if not features:
        raise RuntimeError("Не удалось получить границы регионов из Overpass")

    gdf = geopandas.GeoDataFrame.from_features(features, crs="EPSG:4326")

    if len(gdf) < 80:
        raise RuntimeError(f"Загружены не все регионы: {len(gdf)}")

    gdf.to_file(REGIONS_DATA, driver="GeoJSON")

    print(f'{GREEN}Сохранены геоданные регионов: {REGIONS_DATA}{RESET}')


def download_lakes(API, LAKES_DATA, REGIONS_DATA):
    print('Загрузка озер с Overpass (может занять несколько минут)...')
    result = overpass_request(API, LAKES_QUERY).content.decode("utf-8")

    if not result.startswith("@type"):
        raise RuntimeError(f'Overpass вернул ошибку:\n{result[:50]}')
    else:
        print(f'{GREEN}Получены данные озер c Overpass{RESET}')

    lakes_df = read_csv(StringIO(result), sep=';')
    lakes_df = lakes_df.dropna(subset=["@lat", "@lon"]).copy()

    print(f'Находим их регионы...')
    lakes_data = attach_regions(lakes_df, REGIONS_DATA)

    lakes_data.to_csv(LAKES_DATA,
                      index=False,
                      sep=';',
                      encoding="utf-8")

    print(f'{GREEN}Сохранены озера: {LAKES_DATA}{RESET}')
