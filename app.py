import streamlit as st
import pandas as pd
from sidebar import show_sidebar, sidebar_filters
from dashboard import show_overview_dashboard, show_trends_over_time, show_demographic_insights, \
                      show_expenditure_analysis, show_mortality_trends, show_comparative_insights, \
                      show_key_indicator_highlights, \
                      show_maternal_child_piecharts, show_infectious_diseases_piecharts, \
                      show_nutrition_foodsecurity_piecharts, show_expenditure_piecharts, \
                      show_population_piecharts, show_mortality_piecharts
from about import show_about, show_sri_lanka_map
from categories import map_category  
from visualizations import show_animated_line_chart, show_radar_chart, show_stacked_area_chart, show_bullet_graph

health = pd.read_csv("Sri Lanka Health Statistics.csv")
health['Category'] = health['Indicator Name'].apply(map_category)

def main():
    page = show_sidebar()
    category, selected_indicators, year_range, sort_order, keyword_filter = sidebar_filters(health)
    
    filtered_health = health[
        (health['Year'].between(year_range[0], year_range[1])) &
        (health['Indicator Name'].str.contains(keyword_filter, case=False) if keyword_filter != "All" else True)
    ]
    
    if page == "About":
        show_about()
        show_sri_lanka_map()
    elif page == "Overview Dashboard":
        show_overview_dashboard(filtered_health)
    elif page == "Trends Over Time":
        show_trends_over_time(filtered_health)
        show_animated_line_chart(filtered_health)
    elif page == "Demographic Insights":
        show_demographic_insights(filtered_health)
        show_stacked_area_chart(filtered_health)
    elif page == "Expenditure Analysis":
        show_expenditure_analysis(filtered_health)
        show_stacked_area_chart(filtered_health)
    elif page == "Mortality & Morbidity":
        show_mortality_trends(filtered_health)
    elif page == "Comparative Insights":
        show_comparative_insights(filtered_health)
        show_radar_chart(filtered_health, category)
    elif page == "Key Indicator Highlights":
        show_key_indicator_highlights(filtered_health)
    if selected_indicators:
        for indicator in selected_indicators:
            show_bullet_graph(filtered_health, indicator, 75, year_range)
    elif page == "Maternal and Child Health":
        show_maternal_child_piecharts(filtered_health)
    elif page == "Infectious Diseases":
        show_infectious_diseases_piecharts(filtered_health)
    elif page == "Nutrition and Food Security":
        show_nutrition_foodsecurity_piecharts(filtered_health)
    elif page == "Health Expenditures":
        show_expenditure_piecharts(filtered_health)
    elif page == "Population Health and Demographics":
        show_population_piecharts(filtered_health)
    elif page == "Mortality Rates":
        show_mortality_piecharts(filtered_health)

if __name__ == "__main__":
    main()