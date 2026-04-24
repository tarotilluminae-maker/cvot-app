import streamlit as st
from geopy.geocoders import Nominatim
import math
import pandas as pd

from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

st.set_page_config(page_title="CVOT Engine", layout="wide")

st.title("CVOT Forensic Astrology Engine")

# ---------------- INPUT ----------------
birth_date = st.text_input("Birth Date (YYYY/MM/DD)")
birth_time = st.text_input("Birth Time (HH:MM)")
birth_location = st.text_input("Birth Location")

last_known_location = st.text_input("Last Known Location")

# ---------------- GEO ----------------
@st.cache_data
def get_location(loc_input):
    geo = Nominatim(user_agent="cvot")
    return geo.geocode(loc_input)

# ---------------- CORE ----------------
def project(lat, lon, bearing, distance):
    R = 6371
    br = math.radians(bearing)
    new_lat = lat + (distance / R) * math.cos(br)
    new_lon = lon + (distance / R) * math.sin(br)
    return new_lat, new_lon

def cluster_points(df):
    # simple clustering by rounding (fast + effective v1)
    df["cluster_lat"] = df["lat"].round(2)
    df["cluster_lon"] = df["lon"].round(2)
    grouped = df.groupby(["cluster_lat", "cluster_lon"]).size().reset_index(name="weight")
    return grouped.sort_values("weight", ascending=False)

# ---------------- RUN ----------------
if st.button("Run CVOT"):

    if not all([birth_date, birth_time, birth_location, last_known_location]):
        st.error("Fill all fields")
        st.stop()

    birth_geo = get_location(birth_location)
    last_geo = get_location(last_known_location)

    if not birth_geo or not last_geo:
        st.error("Location error")
        st.stop()

    try:
        date = Datetime(birth_date, birth_time, '+00:00')
        pos = GeoPos(str(birth_geo.latitude), str(birth_geo.longitude))
        chart = Chart(date, pos)

        # PLANETS + WEIGHTS (real logic layer)
        planet_weights = {
            const.SUN: 3,
            const.MOON: 4,
            const.MERCURY: 2,
            const.VENUS: 2,
            const.MARS: 5,
            const.JUPITER: 3,
            const.SATURN: 4
        }

        base_lat, base_lon = last_geo.latitude, last_geo.longitude

        points = []
        vectors = []

        for p, weight in planet_weights.items():
            obj = chart.get(p)
            bearing = obj.lon % 360

            vectors.append({
                "Planet": p,
                "Degree": round(obj.lon, 2),
                "Bearing": round(bearing, 2),
                "Weight": weight
            })

            # multiple projections = stronger influence
            for i in range(weight):
                dist = 20 + (i * 5)
                lat, lon = project(base_lat, base_lon, bearing, dist)

                points.append({
                    "lat": lat,
                    "lon": lon,
                    "planet": p
                })

        df_points = pd.DataFrame(points)

        # ---------------- CLUSTERING ----------------
        clusters = cluster_points(df_points)

        # ---------------- OUTPUT ----------------
        st.subheader("Planetary Vectors")
        st.dataframe(pd.DataFrame(vectors), use_container_width=True)

        st.subheader("High Probability Zones")
        st.dataframe(clusters.head(10), use_container_width=True)

        st.subheader("Map (All Vectors)")
        st.map(df_points)

        st.subheader("Map (Top Clusters)")
        st.map(clusters.rename(columns={"cluster_lat": "lat", "cluster_lon": "lon"}))

        st.success("CVOT Analysis Complete")

    except Exception as e:
        st.error(str(e))
