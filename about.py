import streamlit as st

def show_about():
    bg_image_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/About.jpg"

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
        h1, h2, h3, h4, h5, h6 {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("About This Dashboard")
    st.markdown("""
    ## Sri Lanka Health Insights Dashboard

    This interactive dashboard provides comprehensive visualization of national health indicators from 1960 to 2023.

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

    Data Sources: World Bank, Sri Lanka Health Ministry, and WHO datasets.
    """)

def show_sri_lanka_map():
    st.markdown("### Geographic Context")
    st.image("https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Map%20or%20Sri%20Lanka.png", 
            use_column_width=True)
    st.markdown("The map provides geographic reference for regional health variations across Sri Lanka.")