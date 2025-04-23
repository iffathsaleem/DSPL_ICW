import streamlit as st
import pandas as pd

def show_about():
    bg_image_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/About.jpg"

    # Add background and dark overlay
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(
                rgba(0, 0, 0, 0.7), 
                rgba(0, 0, 0, 0.7)
            ), url("{bg_image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: white;
        }}
        .block-container {{
            background-color: rgba(0, 0, 0, 0);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("About This Dashboard")
    st.markdown("""
    Welcome to the **Sri Lanka Health Insights Dashboard**.  
    This platform visualizes national health data from **1960 to 2023**, offering insights across:

    - Maternal and child health  
    - Infectious diseases and immunization  
    - Nutrition and food security  
    - Health expenditure  
    - Population demographics  
    - Mortality and life expectancy  

    ### Features:
    - Interactive charts and visual breakdowns  
    - Keyword + category filtering (e.g., “female”, “kids”)  
    - Time-range comparisons  
    - Pie, line, and bar visualizations  

    **Built for data-driven insights and public health understanding.**
    """)

import streamlit as st
import folium
from streamlit_folium import st_folium

def show_sri_lanka_map():
    st.markdown("### Map of Sri Lanka")
    st.image("https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Map%20or%20Sri%20Lanka.png", use_column_width=True)