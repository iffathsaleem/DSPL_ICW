import streamlit as st
from visualizations import show_interactive_map

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
 
    # About Section
    with st.container():
        st.markdown('<div class="about-container">', unsafe_allow_html=True)
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

        **Data Sources:** World Bank, Sri Lanka Health Ministry, and WHO datasets.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # Map Section
    with st.container():
        st.markdown('<div class="about-container">', unsafe_allow_html=True)
        st.subheader("Geographic Context")
        st.markdown("The map below provides geographic reference for regional health variations across Sri Lanka.")
        show_interactive_map()
        st.markdown('</div>', unsafe_allow_html=True)
