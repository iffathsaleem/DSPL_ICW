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

    **Dashboard Features:**
    - View and compare health indicators over time
    - Pie chart summaries of indicator contributions
    - Line charts and data tables
    - Filter indicators by category, keyword (e.g. 'kids', 'female', etc.), year range, and sorting order
    """)
