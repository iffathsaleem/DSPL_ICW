import streamlit as st
import pandas as pd
from sidebar import show_sidebar, set_section_background, SECTION_BACKGROUNDS
from dashboard import (
    show_overview,
    show_health_expenditure_insights,
    show_category_analysis
)
from about import show_about
from categories import categories, map_category
from visualizations import show_interactive_map, show_comparative_section
from summary import show_summary 

@st.cache_data
def load_data():
    try:
        health = pd.read_csv("Sri Lanka Health Statistics.csv")
        health["Value"] = pd.to_numeric(health["Value"], errors='coerce')
        health["Year"] = health["Year"].astype(int)
        health["Category"] = health["Indicator Name"].apply(map_category)
        return health[health["Category"] != "Other"]
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def apply_filters(data, filters):
    if not filters or data.empty:
        return data
    
    filtered = data[
        data['Year'].between(filters['year_range'][0], filters['year_range'][1])
    ]
    
    if filters.get('categories'):
        filtered = filtered[filtered['Category'].isin(filters['categories'])]
    
    return filtered.sort_values("Year")

def footer():
    st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(0,0,0,0.7);
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        z-index: 1000;
    }
    </style>
    <div class="footer">
        Developed for Individual Coursework for Data Science Project Lifecycle Module | University of Westminster
    </div>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        layout="wide",
        page_title="Sri Lanka Health Dashboard",
        page_icon="🇱🇰"
    )
    
    health_data = load_data()
    page, filters = show_sidebar(health_data)
    
    if any(page.startswith(cat) for cat in categories.keys()):
        set_section_background(page)
    
    filtered_data = apply_filters(health_data, filters)

    if page == "About":
        show_about()
    elif page == "Overview":
        show_overview(health_data)
    elif page == "Executive Summary": 
        show_summary() 
    elif page == "Comparative Insights":
        show_comparative_section(health_data)
    elif any(page.startswith(cat) for cat in categories.keys()):
        category_name = page.replace(" Analysis", "")
        show_category_analysis(health_data, category_name)
    else:
        st.error(f"Page '{page}' not configured")
    
    footer()

if __name__ == "__main__":
    main()