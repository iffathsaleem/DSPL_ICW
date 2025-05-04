import streamlit as st
from visualizations import show_interactive_map
def show_about():
    bg_image_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/About.jpg"
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url("{bg_image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .block-container {{
            background-color: rgba(0, 0, 0, 0);
        }}
        h1, h2, h3, h4, h5, h6, p, li, div {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
 
    with st.container():
        st.title("About This Dashboard")
        st.markdown("""
        ## Sri Lanka Health Insights Dashboard
        This interactive dashboard provides comprehensive visualization of national health indicators from 1960 to 2023.
        ### Key Focus Areas:
        - Mortality Rates  
        - Maternal and Child Health  
        - Infectious Diseases  
        - Health Expenditure  
        - Healthcare Infrastructure and Services  
        - Water, Sanitation, and Hygiene  
        - Non-communicable Diseases and Risk Factors  
        - Nutrition and Food Security  
        - Demographic Indicators  
        - Reproductive Health  
        - Civil Registration  
        - Injury and External Causes  
        ### Main Features:
        - Interactive charts and visualizations  
        - Advanced filtering by category and keywords  
        - Time-series analysis across decades  
        - Key performance indicators tracking  
        - Comparative insights across indicators  
        **Data Sources:** World Bank datasets.
        """)
    with st.container():
        show_interactive_map()