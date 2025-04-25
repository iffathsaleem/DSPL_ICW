import streamlit as st
import pandas as pd
from sidebar import show_sidebar, sidebar_filters
from dashboard import (
    show_overview_stats,
    show_trends_over_time,
    show_demographic_and_population_insights,
    show_health_expenditure_insights,
    show_mortality_and_morbidity_trends,
    show_comparative_insights,
    show_key_indicator_highlights,
    show_maternal_child_piecharts,
    show_infectious_diseases_piecharts,
    show_nutrition_foodsecurity_piecharts,
    show_expenditure_piecharts,
    show_population_piecharts,
    show_mortality_piecharts,
    initialize_page
)
from about import show_about, show_sri_lanka_map
from visualizations import (
    show_animated_line_chart,
    show_radar_chart,
    show_stacked_area_chart,
    show_bullet_graph,
    show_pie_chart,
    show_trend_chart
)
from categories import map_category

def load_data():
    try:
        health = pd.read_csv("Sri Lanka Health Statistics.csv")
        health['Category'] = health['Indicator Name'].apply(map_category)
        return health
    except FileNotFoundError:
        st.error("Error: Data file not found. Please ensure 'Sri Lanka Health Statistics.csv' exists in the project directory.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def main():
    health = load_data()
    if health.empty:
        st.warning("Unable to load data. Please check the error message above.")
        return

    st.set_page_config(
        layout="wide",
        page_title="Sri Lanka Health Dashboard",
        page_icon="🇱🇰"
    )

    page = show_sidebar()
    category, selected_indicators, year_range, sort_order, keyword_filter = sidebar_filters(health)
    
    filtered_health = health[
        (health['Year'].between(year_range[0], year_range[1])) &
        (health['Indicator Name'].str.contains(keyword_filter, case=False) if keyword_filter != "All" else True)
    ].sort_values("Year", ascending=sort_order == "Oldest to Newest")

    # Page routing
    if page == "About":
        show_about()
        show_sri_lanka_map()
    
    elif page == "Overview Dashboard":
        show_overview_stats(filtered_health)
    
    elif page == "Trends Over Time":
        show_trends_over_time(filtered_health, selected_indicators)
    
    elif page == "Demographic and Population Insights":
        initialize_page("Demographic and Population Insights")
        show_demographic_and_population_insights(filtered_health)
        show_stacked_area_chart(filtered_health)
        show_population_piecharts(filtered_health)
    
    elif page == "Health Expenditure Insights":
        initialize_page("Health Expenditure Insights")
        show_health_expenditure_insights(filtered_health)
        show_expenditure_piecharts(filtered_health)
    
    elif page == "Mortality and Morbidity Trends":
        initialize_page("Mortality and Morbidity Trends")
        show_mortality_and_morbidity_trends(filtered_health)
        show_mortality_piecharts(filtered_health)
    
    elif page == "Comparative Insights":
        initialize_page("Comparative Insights")
        show_comparative_insights(filtered_health)
        if category in categories:
            show_radar_chart(filtered_health, category)
    
    elif page == "Key Indicator Highlights":
        initialize_page("Key Indicator Highlights")
        show_key_indicator_highlights(filtered_health)
        if selected_indicators:
            for indicator in selected_indicators:
                show_bullet_graph(filtered_health, indicator, 75, year_range)
    
    elif page == "Maternal and Child Health":
        initialize_page("Maternal and Child Health")
        show_maternal_child_piecharts(filtered_health)
        show_pie_chart(filtered_health, "Maternal and Child Health")
    
    elif page == "Infectious Diseases":
        initialize_page("Infectious Diseases")
        show_infectious_diseases_piecharts(filtered_health)
        show_pie_chart(filtered_health, "Infectious Diseases")
    
    elif page == "Nutrition and Food Security":
        initialize_page("Nutrition and Food Security")
        show_nutrition_foodsecurity_piecharts(filtered_health)
        show_pie_chart(filtered_health, "Nutrition and Food Security")

if __name__ == "__main__":
    main()