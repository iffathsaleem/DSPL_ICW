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
            ...
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
