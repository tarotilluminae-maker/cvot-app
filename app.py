import streamlit as st
from geopy.geocoders import Nominatim
import math
import pandas as pd

# -------------------------------
# UI HEADER
# -------------------------------
st.set_page_config(layout="wide")
st.title("CVOT Analysis Engine (No-Code Version)")

# -------------------------------
# INPUT SECTION
# -------------------------------
st.sidebar.header("Input Data")

birth_date = st.sidebar.text_input("Birth Date (YYYY-MM-DD)")
birth_time = st.sidebar.text_input("Birth Time (HH:MM)")
birth_location = st.sidebar.text_input("Birth Location")

last_known_location = st.sidebar.text_input("Last Known Location")
timestamp = st.sidebar.text_input("Timestamp (YYYY-MM-DD)")
case_context = st.sidebar.text_area("Case Context")

# -------------------------------
# CORE RULES DATA
# -------------------------------
TERRAIN_MAP = {
    "Mars
