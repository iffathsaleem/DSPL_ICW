import streamlit as st
from visualizations import show_interactive_map

def show_about():
    bg_image_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/About.jpg"

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] > .main {{
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
        [data-testid="stHeader"] {{
            background: rgba(0, 0, 0, 0);
        }}
        [data-testid="stSidebar"] {{
            background: rgba(0, 0, 0, 0.5);
        }}
        h1, h2, h3, h4, h5, h6, p {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("About This Dashboard")
    st.markdown(""" 
    ## Sri Lanka Health Insights Dashboard

    This interactive dashboard provides a comprehensive visualization of national health indicators from **1960 to 2023**.

    ### Key Focus Areas:
    - Maternal and child health  
    - Infectious diseases and immunization  
    - Nutrition and food security  
    - Health expenditure analysis  
    - Population demographics  
    - Mortality and life expectancy trends  

    ### Main Features:
    - Interactive charts and visualizations  
    - Advanced filtering by category and keywords  
    - Time-series analysis across decades  
    - Key performance indicators tracking  
    - Comparative insights across indicators  

    **Data Sources:** World Bank, Sri Lanka Health Ministry, and WHO datasets.
    """)
