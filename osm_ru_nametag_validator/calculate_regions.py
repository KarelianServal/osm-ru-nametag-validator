import geopandas


def _load_regions(REGIONS_DATA):
    regions = geopandas.read_file(REGIONS_DATA)

    if regions.crs is None:
        regions = regions.set_crs("EPSG:4326")
    elif regions.crs != "EPSG:4326":
        regions = regions.to_crs("EPSG:4326")

    regions = geopandas.read_file(REGIONS_DATA)

    regions = regions[regions.geometry.notna() & ~regions.geometry.is_empty]
    regions = regions.set_geometry(regions.geometry.make_valid())
    regions = regions.explode(index_parts=False)
    regions = regions[
        regions.geometry.geom_type.isin(["Polygon", "MultiPolygon"])
    ]

    name, name_ru = regions.get("name"), regions.get("name:ru")
    if name_ru is not None:
        regions["region"] = name_ru.fillna(regions["name"])
    elif name is not None:
        regions["region"] = regions["name"]
    else:
        raise KeyError("В файле регионов нет колонок name / name:ru")

    return regions[["region", "geometry"]]


def attach_regions(lakes_df, REGIONS_DATA):
    print('Находим регионы озер...')

    lakes_df = lakes_df.dropna(subset=["@lat", "@lon"]).copy()
    lakes_gdf = geopandas.GeoDataFrame(
        lakes_df,
        geometry=geopandas.points_from_xy(lakes_df["@lon"],
                                          lakes_df["@lat"]),
        crs="EPSG:4326",
    )

    regions = _load_regions(REGIONS_DATA)

    joined = geopandas.sjoin(
        lakes_gdf,
        regions,
        how="left",
        predicate="intersects",
    )

    joined = joined.sort_values("region", na_position="last")
    joined = joined.drop_duplicates(subset=["@type", "@id"])

    print('Регионы озер успешно найдены')
    return joined[["@type", "@id", "name", "region", "@lat", "@lon"]]

