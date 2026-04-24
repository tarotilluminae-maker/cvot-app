import streamlit as st
from geopy.geocoders import Nominatim
import math
import pandas as pd

st.set_page_config(page_title="CVOT Engine", layout="centered")

st.title("CVOT Analysis Engine")

# INPUT
location_input = st.text_input("Last Known Location")

# CACHE (makes it fast)
@st.cache_data
def get_location(loc_input):
    geo = Nominatim(user_agent="cvot")
    return geo.geocode(loc_input)

def project(lat, lon, bearing, distance):
    R = 6371
    bearing_rad = math.radians(bearing)
    new_lat = lat + (distance / R) * math.cos(bearing_rad)
    new_lon = lon + (distance / R) * math.sin(bearing_rad)
    return new_lat, new_lon

# RUN BUTTON
if st.button("Run CVOT Analysis"):

    loc = get_location(location_input)

    if not loc:
        st.error("Location not found")
    else:
        lat, lon = loc.latitude, loc.longitude

        st.subheader("Results")

        bearings = [45, 180, 300]
        results = []

        for i, b in enumerate(bearings):
            new_lat, new_lon = project(lat, lon, b, 25)

            results.append({
                "Zone": i + 1,
                "Latitude": round(new_lat, 5),
                "Longitude": round(new_lon, 5)
            })

        # CLEAN DISPLAY
        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)

        # MAP
        st.subheader("Map View")
        st.map(df.rename(columns={"Latitude": "lat", "Longitude": "lon"}))

        st.success("Analysis complete")
