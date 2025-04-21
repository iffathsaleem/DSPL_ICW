import streamlit as st
import folium
from streamlit.components.v1 import html

def show_about():
    st.markdown(
        """
        <style>
        /* Style for full background image with 50% opacity */
        .about-background {
            background-image: url('public-service-img-new1-scaled.jpg');
            background-size: cover;
            background-position: center;
            height: 100vh;  /* Full screen height */
            width: 100%;  /* Full screen width */
            position: fixed; /* Fix the image behind the content */
            top: 0;
            left: 0;
            z-index: -1;  /* Ensure the image is behind the content */
            opacity: 0.5;  /* 50% transparency */
        }

        /* Content style */
        .content {
            position: relative;
            z-index: 1;
            color: white;
            padding: 20px;
            font-size: 18px;
            line-height: 1.6;
        }

        /* Ensure the map has space */
        .map-container {
            margin-top: 30px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Title and description for the About page
    st.markdown('<div class="about-background"></div>', unsafe_allow_html=True)
    
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
    
    sri_lanka_coords = [7.8731, 80.7718]  

    # Create the map centered at Sri Lanka
    sri_lanka_map = folium.Map(location=sri_lanka_coords, zoom_start=7)  

    locations = [
        {"name": "Colombo", "coords": [6.9271, 79.8612]},  # Colombo
        {"name": "Kandy", "coords": [7.2906, 80.6337]},    # Kandy
        {"name": "Galle", "coords": [6.0535, 80.2200]},    # Galle
        {"name": "Jaffna", "coords": [9.6690, 80.0228]},   # Jaffna
    ]
    
    for location in locations:
        folium.Marker(location["coords"], popup=location["name"]).add_to(sri_lanka_map)
    
    st.markdown("### Interactive Map of Sri Lanka", unsafe_allow_html=True)

    map_html = sri_lanka_map._repr_html_()  
    html(map_html, height=600)

    st.markdown('</div>', unsafe_allow_html=True)
