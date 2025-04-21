# Section 1: About

import streamlit as st

def show_about():
    st.title("About This Dashboard")
    st.markdown("""
    This dashboard presents health indicators for **Sri Lanka** from **1960 to 2023**. It covers a wide range of topics:
    
    - Fertility and birth rates
    - Mortality and life expectancy
    - Infectious diseases and HIV
    - Maternal and child health
    - Health expenditure
    - Access to healthcare and sanitation

    Use the sidebar to:
    - Select indicator categories
    - Filter by year or a custom year range
    - View trends and make comparisons

    ---
    """)
