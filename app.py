import streamlit as st
import pandas as pd
from sidebar import show_sidebar
from dashboard import (
    show_overview,
    show_demographic_and_population_insights,
    show_health_expenditure_insights,
    show_mortality_and_morbidity_trends,
    show_comparative_insights,
    show_key_indicator_highlights,
    show_category_analysis
)
from about import show_about, show_interactive_map
from categories import categories, map_category
from visualizations import show_data_explorer

@st.cache_data
def load_data():
    try:
        health = pd.read_csv("Sri Lanka Health Statistics.csv")
        health["Value"] = pd.to_numeric(health["Value"], errors='coerce')
        health["Year"] = health["Year"].astype(int)
        health["Category"] = health["Indicator Name"].apply(map_category)
        
        # Validate required columns exist
        required_columns = ['Indicator Name', 'Year', 'Value', 'Category']
        if not all(col in health.columns for col in required_columns):
            st.error("Data file is missing required columns.")
            return pd.DataFrame()
            
        return health[health["Category"] != "Other"]
        
    except FileNotFoundError:
        st.error("Data file not found. Please ensure 'Sri Lanka Health Statistics.csv' exists.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def initialize_default_filters(health_data):
    """Initialize default filter values based on data"""
    if health_data.empty:
        return {
            'year_range': (2000, 2023),
            'indicators': [],
            'keyword': "All",
            'category': "All",
            'sort_order': "Ascending"
        }
    
    years = sorted(health_data['Year'].unique())
    return {
        'year_range': (int(min(years)), int(max(years))),
        'indicators': [],
        'keyword': "All",
        'category': "All",
        'sort_order': "Ascending"
    }

def apply_filters(data, filters):
    """Apply filters from session state to the data"""
    if not filters or data.empty:
        return data
    
    filtered = data.copy()
    
    # Apply year filter
    filtered = filtered[
        filtered['Year'].between(filters['year_range'][0], filters['year_range'][1])
    ]
    
    # Apply indicator filter if any selected
    if filters.get('indicators'):
        filtered = filtered[filtered['Indicator Name'].isin(filters['indicators'])]
    
    # Apply keyword filter
    if filters.get('keyword') and filters['keyword'] != "All":
        filtered = filtered[
            filtered['Indicator Name'].str.contains(filters['keyword'], case=False)
        ]
    
    # Apply category filter
    if filters.get('category') and filters['category'] != "All":
        filtered = filtered[filtered['Category'] == filters['category']]
    
    # Apply sorting
    sort_ascending = filters.get('sort_order', "Ascending") == "Ascending"
    return filtered.sort_values("Year", ascending=sort_ascending)

def main():
    # Initialize page config first
    st.set_page_config(
        layout="wide",
        page_title="Sri Lanka Health Dashboard",
        page_icon="🇱🇰"
    )
    
    # Load data
    health_data = load_data()
    
    # Initialize default filters if they don't exist
    if 'current_filters' not in st.session_state:
        st.session_state.current_filters = initialize_default_filters(health_data)
    
    # Show sidebar and get current page
    page = show_sidebar(health_data)
    
    # Get filtered data
    filtered_data = apply_filters(
        health_data,
        st.session_state.get('current_filters', {})
    )

    # Page routing
    if page == "About":
        show_about()
        show_interactive_map(health_data)  
    elif page == "Overview":
        show_overview(health_data)  
    elif page == "Population Health and Demographics":
        show_demographic_and_population_insights(filtered_data)
    elif page == "Health Expenditures":
        show_health_expenditure_insights(filtered_data)
    elif page == "Mortality Rates":
        show_mortality_and_morbidity_trends(filtered_data)
    elif page == "Comparative Insights":
        show_comparative_insights(filtered_data)
    elif page == "Key Indicator Highlights":
        show_key_indicator_highlights(filtered_data)
    elif page == "Data Explorer":
        show_data_explorer(filtered_data)
    elif page == "Forecasting":
        show_forecasting(filtered_data)
    elif page in categories:
        show_category_analysis(filtered_data, page)

if __name__ == "__main__":
    main()