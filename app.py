import streamlit as st
import pandas as pd
import plotly.express as px

health = pd.read_csv("Sri Lanka Health Statistics.csv")

st.title("Sri Lankan Health Indicators Dashboard")

# Indicator selection 
indicators = st.sidebar.multiselect(
    "Select Health Indicators",
    health["Indicator Name"].unique(),
    default=["Life expectancy at birth, total (years)"]
)

# Year selection 
year_selection_mode = st.sidebar.radio("Select Year Mode", ["Single Year", "Year Range"])

if year_selection_mode == "Single Year":
    year = st.sidebar.selectbox("Select Year", sorted(health["Year"].unique()))
    selected_years = (year, year)
else:
    selected_years = st.sidebar.slider(
        "Select Year Range",
        min_value=int(health["Year"].min()),
        max_value=int(health["Year"].max()),
        value=(1960, 2023)
    )

