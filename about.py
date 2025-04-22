import streamlit as st
import pandas as pd

def show_about():
    bg_image_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/public-service-img-new1-scaled.jpg"
    sidebar_bg_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/png-transparent-medicine-health-care-logo-health-love-text-heart-thumbnail.png"

    # Add page background and sidebar background
    st.markdown(
        f"""
        <style>
        /* Main background with overlay */
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

        /* Sidebar background with overlay */
        [data-testid="stSidebar"] {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
                              url('{sidebar_bg_url}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        /* White text for sidebar elements */
        .stSelectbox div[data-baseweb="select"],
        .stMultiSelect div[data-baseweb="select"],
        .stSlider,
        .stRadio,
        .css-1cpxqw2, .css-1v0mbdj, .css-1r6slb0,
        label, .css-10trblm, .css-qrbaxs, .css-16huue1 {{
            color: white !important;
        }}

        .css-1n76uvr, .css-1p3m7a8 {{
            background-color: #444 !important;
            color: white !important;
            border: 1px solid white !important;
        }}

        .stSelectbox > div > div,
        .stMultiSelect > div > div {{
            color: white !important;
        }}

        .css-1wa3eu0-option {{
            color: black !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("About This Dashboard")
    st.markdown("""
    This dashboard presents health indicators for **Sri Lanka** from **1960 to 2023**. It covers a wide range of topics:

    - Fertility and birth rates  
    - Mortality and life expectancy  
    - Infectious diseases and HIV  
    - Maternal and child health  
    - Health expenditure  
    - Access to healthcare and sanitation  

    **Dashboard Features:**  
    - View and compare health indicators over time  
    - Pie chart summaries of indicator contributions  
    - Line charts and data tables  
    - Filter indicators by category, keyword (e.g. 'kids', 'female', etc.), year range, and sorting order  
    """)

    st.markdown("### Interactive Map of Sri Lanka")
    df = pd.DataFrame({
        'latitude': [7.8731],
        'longitude': [80.7718]
    })
    st.map(df)
