import streamlit as st
import pandas as pd
from sidebar import sidebar_filters
from about import show_about
from dashboard import show_dashboard

# Load your health data from specified path
health = pd.read_csv("C:/Users/HP/OneDrive - University of Westminster/L5/Semester 2/Data Science Project Lifecycle/CW 2/HEALTH/DSPL_ICW/data/health_data.csv")

# Sidebar navigation
st.sidebar.title("Navigation")
view = st.sidebar.radio("Go to", ["About", "Dashboard"])

if view == "About":
    show_about()
elif view == "Dashboard":
    category, selected_indicators, year_range, sort_order, keyword_filter = sidebar_filters(health)
    show_dashboard(health, category, selected_indicators, year_range, sort_order, keyword_filter)
