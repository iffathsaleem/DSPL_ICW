import streamlit as st
import folium
from streamlit.components.v1 import html

def show_about():
    st.markdown(
        """
        <style>
        .about-background {
            background-image: url('public-service-img-new1-scaled.jpg');
            background-size: cover;
            background-position: center;
            height: 100vh;
            position: absolute;
            width: 100%;
            z-index: -1;
            opacity: 0.5;
        }
        .content {
            position: relative;
            z-index: 1;
            color: white;
            padding: 20px;
        }
        </style>
        """, unsafe_allow_html=True
    )
    
    st.markdown('<div class="about-background"></div>', unsafe_allow_html=True)

    # Title and description for the About page 
    st.markdown('<div class="content">', unsafe_allow_html=True)
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

    # Create an interactive map of Sri Lanka using folium
    sri_lanka_map = folium.Map(location=[7.8731, 80.7718], zoom_start=7)  # Coordinates for Sri Lanka

    # Marker at the center of Sri Lanka
    folium.Marker([7.8731, 80.7718], popup="Sri Lanka").add_to(sri_lanka_map)

    st.markdown("### Interactive Map of Sri Lanka")

    map_html = sri_lanka_map._repr_html_()  
    html(map_html, height=600)  

    # Close the content div
    st.markdown('</div>', unsafe_allow_html=True)
