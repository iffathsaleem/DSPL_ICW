import streamlit as st
import pandas as pd

def show_about():
    bg_image_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/public-service-img-new1-scaled.jpg"

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
    health = pd.DataFrame({
        'latitude': [7.8731],
        'longitude': [80.7718]
    })
    st.map(health)
