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
        
        # Student Details Section
        st.markdown("""
        <div style="background-color: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="color: white; margin-top: 0;">Student Details</h3>
            <p style="color: white; margin-bottom: 5px;"><strong>Name:</strong> Iffath Saleem</p>
            <p style="color: white; margin-bottom: 5px;"><strong>IIT ID:</strong> 20231818</p>
            <p style="color: white; margin-bottom: 0;"><strong>UOW ID:</strong> W205156</p>
        </div>
        """, unsafe_allow_html=True)
        
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
        
        **Data Sources:** World Bank datasets
        """)
    
    with st.container():
        st.markdown("---")
        st.header("Geographical Context")
        show_interactive_map()