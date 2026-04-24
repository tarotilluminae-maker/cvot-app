import streamlit as st
from geopy.geocoders import Nominatim
import math

st.title("CVOT Analysis Engine")

location_input = st.text_input("Last Known Location")

def project(lat, lon, bearing, distance):
    R = 6371
    bearing_rad = math.radians(bearing)
    new_lat = lat + (distance / R) * math.cos(bearing_rad)
    new_lon = lon + (distance / R) * math.sin(bearing_rad)
    return new_lat, new_lon

if st.button("Run"):

    geo = Nominatim(user_agent="cvot")
    loc = geo.geocode(location_input)

    if not loc:
        st.error("Location not found")
    else:
        lat, lon = loc.latitude, loc.longitude

        st.write("### Results")

        bearings = [45, 180, 300]

        for i, b in enumerate(bearings):
            new_lat, new_lon = project(lat, lon, b, 25)

            st.write({
                "zone": i+1,
                "coordinates": (round(new_lat, 5), round(new_lon, 5))
            })
