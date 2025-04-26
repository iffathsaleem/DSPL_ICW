import streamlit as st
import pandas as pd
from sidebar import show_sidebar, sidebar_filters
from dashboard import (
    show_overview,
    show_demographic_and_population_insights,
    show_health_expenditure_insights,
    show_mortality_and_morbidity_trends,
    show_comparative_insights,
    show_key_indicator_highlights,
    show_category_analysis
)
from about import show_about, show_sri_lanka_map
from categories import categories, map_category

@st.cache_data
def load_data():
    try:
        health = pd.read_csv("Sri Lanka Health Statistics.csv")
        health['Value'] = pd.to_numeric(health['Value'], errors='coerce')
        health['Year'] = health['Year'].astype(int)
        health['Category'] = health['Indicator Name'].apply(map_category)
        return health[health['Category'] != "Other"]
    except FileNotFoundError:
        st.error("Data file not found. Please ensure the CSV exists.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def main():
    health_data = load_data()
    if health_data.empty:
        return

    page = show_sidebar()
    category, selected_indicators, year_range, sort_order, keyword_filter = sidebar_filters(health_data)
    
    filtered_data = health_data[
        (health_data['Year'].between(year_range[0], year_range[1])) &
        (health_data['Indicator Name'].str.contains(keyword_filter, case=False) if keyword_filter != "All" else True)
    ].sort_values("Year", ascending=sort_order == "Oldest to Newest")

    if page == "About":
        show_about()
        show_sri_lanka_map()
    elif page == "Overview":
        show_overview(filtered_data)
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
    elif page in categories:
        show_category_analysis(filtered_data, page)

if __name__ == "__main__":
    st.set_page_config(
        layout="wide",
        page_title="Sri Lanka Health Dashboard",
        page_icon="🇱🇰"
    )
    main()