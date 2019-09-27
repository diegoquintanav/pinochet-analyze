import logging

import folium
from folium.plugins import Search
import pandas as pd
import geopandas as gpd
import numpy

DATASET_PATH = "/src/data/pinochet.csv"
INITIAL_ZOOM = [-33.501342, -70.654242]

logger = logging.getLogger()


def get_data():
    df = pd.read_csv(DATASET_PATH, sep=",", header=0)
    dfn1 = df.drop(
        axis=1,
        labels=[
            "place_2",
            "location_2",
            "latitude_2",
            "longitude_2",
            "exact_coordinates_2",
            "place_3",
            "end_location_3",
            "latitude_3",
            "longitude_3",
            "exact_coordinates_3",
            "place_4",
            "end_location_4",
            "latitude_4",
            "longitude_4",
            "exact_coordinates_4",
            "place_5",
            "end_location_5",
            "latitude_5",
            "longitude_5",
            "exact_coordinates_5",
            "place_6",
            "end_location_6",
            "latitude_6",
            "longitude_6",
            "exact_coordinates_6",
        ],
    )

    dfn1 = dfn1.dropna(subset=["latitude_1", "longitude_1"])
    gdfn1 = gpd.GeoDataFrame(
        dfn1,
        crs={"init": "epsg:4326"},
        geometry=gpd.points_from_xy(dfn1["longitude_1"], dfn1["latitude_1"]),
    )

    return gdfn1


def style_function(row):
    raise NotImplemented
    return {
        "color": "#0000ff"
        if row["properties"]["method"] == "Gun" is True
        else "#00ff00"
    }


def build_map():

    logger.info("Preparing data")
    data = get_data()

    logger.info("Initializing map")
    m = folium.Map(location=INITIAL_ZOOM, zoom_start=6, tiles="cartodbpositron")

    logger.info("Creating GeoJSON")
    events_map = folium.GeoJson(
        data,
        name="Events documented",
        style_function=None,
        tooltip=folium.GeoJsonTooltip(
            aliases=["Name", "Last Name", "Occupation", "Violence Type"],
            fields=["first_name", "last_name", "occupation", "method"],
            localize=True,
        ),
    ).add_to(m)

    # add a search by first names
    logger.info("Creating search box for names")
    namesearch = Search(
        layer=events_map,
        geom_type="Point",
        placeholder="Escribe un nombre",
        collapsed=False,
        search_label="first_name",
        search_zoom=12,
        #     weight=3
    ).add_to(m)

    # add a search by last name
    logger.info("Creating search box for last names")
    lastnamesearch = Search(
        layer=events_map,
        geom_type="Point",
        placeholder="Escribe un apellido",
        collapsed=False,
        search_label="last_name",
        search_zoom=12,
    ).add_to(m)

    logger.info("Saving to index.html")
    m.save("./index.html")


if __name__ == "__main__":
    build_map()
