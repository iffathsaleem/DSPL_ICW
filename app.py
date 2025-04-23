import streamlit as st
import pandas as pd
from sidebar import show_sidebar, sidebar_filters
from dashboard import show_overview_dashboard, show_trends_over_time, show_demographic_insights, \
                      show_expenditure_analysis, show_mortality_trends, show_comparative_insights, \
                      show_key_indicator_highlights, \
                      show_maternal_child_piecharts, show_infectious_diseases_piecharts, \
                      show_nutrition_foodsecurity_piecharts, show_expenditure_piecharts, \
                      show_population_piecharts, show_mortality_piecharts
from about import show_about
from categories import map_category  

# Load health data
health = pd.read_csv("Sri Lanka Health Statistics.csv")

# Apply category mapping
health['Category'] = health['Indicator Name'].apply(map_category)

def main():
    # Sidebar Navigation
    page = show_sidebar()

    # Filters
    category, selected_indicators, year_range, sort_order, keyword_filter = sidebar_filters(health)

    # Display content based on selection
    if page == "About":
        show_about()
    elif page == "Overview Dashboard":
        show_overview_dashboard(health)
    elif page == "Trends Over Time":
        show_trends_over_time(health)
    elif page == "Demographic Insights":
        show_demographic_insights(health)
    elif page == "Expenditure Analysis":
        show_expenditure_analysis(health)
    elif page == "Mortality & Morbidity":
        show_mortality_trends(health)
    elif page == "Comparative Insights":
        show_comparative_insights(health)
    elif page == "Key Indicator Highlights":
        show_key_indicator_highlights(health)
    elif page == "Maternal and Child Health":
        show_maternal_child_piecharts(health)
    elif page == "Infectious Diseases":
        show_infectious_diseases_piecharts(health)
    elif page == "Nutrition and Food Security":
        show_nutrition_foodsecurity_piecharts(health)
    elif page == "Health Expenditures":
        show_expenditure_piecharts(health)
    elif page == "Population Health and Demographics":
        show_population_piecharts(health)
    elif page == "Mortality Rates":
        show_mortality_piecharts(health)

# Run the app
if __name__ == "__main__":
    main()
