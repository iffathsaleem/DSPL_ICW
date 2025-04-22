import streamlit as st
import pandas as pd
from sidebar import show_sidebar, sidebar_filters
from dashboard import show_overview_dashboard, show_trends_over_time, show_demographic_insights, \
                      show_expenditure_analysis, show_mortality_morbidity, show_comparative_insights, \
                      show_key_indicator_highlights
from about import show_about

# Load your health data from the specified path
health = pd.read_csv("Sri Lanka Health Statistics.csv")

def main():
    # Sidebar Navigation
    page = show_sidebar()

    # Filters (you can keep this inside the main or pass it to each function)
    category, selected_indicators, year_range, sort_order, keyword_filter = sidebar_filters(health)

    # Display content based on selection
    if page == "About":
        show_about()  # This is the correct function name
    elif page == "Overview Dashboard":
        show_overview_dashboard(health)
    elif page == "Trends Over Time":
        show_trends_over_time(health, selected_indicators)
    elif page == "Demographic Insights":
        show_demographic_insights(health)
    elif page == "Expenditure Analysis":
        show_expenditure_analysis(health)
    elif page == "Mortality & Morbidity":
        show_mortality_morbidity(health)
    elif page == "Comparative Insights":
        show_comparative_insights(health)
    elif page == "Key Indicator Highlights":
        show_key_indicator_highlights(health)

if __name__ == "__main__":
    main()
