import streamlit as st
import pandas as pd
from sidebar import sidebar_filters
from about import show_about
from dashboard import show_dashboard

# Sidebar background
def set_sidebar_background(image_url):
    st.markdown(f"""
        <style>
        [data-testid="stSidebar"]::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('{image_url}');
            background-size: cover;
            background-position: center;
            opacity: 0.3;
            z-index: 0;
        }}
        [data-testid="stSidebar"]::after {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 255, 255, 0.7);
            z-index: 1;
        }}
        [data-testid="stSidebar"] * {{
            position: relative;
            z-index: 2;
            color: black !important;
        }}
        </style>
    """, unsafe_allow_html=True)

sidebar_bg_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/png-transparent-medicine-health-care-logo-health-love-text-heart-thumbnail.png"
set_sidebar_background(sidebar_bg_url)

# Load your health data
health = pd.read_csv("Sri Lanka Health Statistics.csv")

# Sidebar navigation
st.sidebar.title("Navigation")
view = st.sidebar.radio("Go to", ["About", "Dashboard"])

if view == "About":
    show_about()
elif view == "Dashboard":
    category, selected_indicators, year_range, sort_order, keyword_filter = sidebar_filters(health)
    show_dashboard(health, category, selected_indicators, year_range, sort_order, keyword_filter)
