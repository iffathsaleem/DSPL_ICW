import streamlit as st
import pandas as pd
from categories import categories, map_category
from visualizations import show_animated_line_chart, show_trend_chart

# Background image configuration
background_images = {
    "About": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/About.jpg",
    "Overview Dashboard": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Overview.jpg",
    "Trends Over Time": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Trends%20Overtime.JPG",
    "Demographic and Population Insights": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Demographic%20Insights.jpg",
    "Health Expenditure Insights": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Expenditure%20Analysis.jpg",
    "Mortality and Morbidity Trends": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Mortality%20%26%20Morbidity.jpg",
    "Comparative Insights": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Comparative%20Insights.jpg",
    "Key Indicator Highlights": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Key%20Indicator%20Highlights.jpg",
    "Maternal and Child Health": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Maternal%20and%20Child%20Health.jpg",
    "Infectious Diseases": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Infectious%20Diseases.jpg",
    "Nutrition and Food Security": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Nutrition%20and%20Food%20Security.jpg"
}

sidebar_image_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Sidebar.png"

def set_sidebar_background(image_url):
    st.markdown(f"""
        <style>
            [data-testid="stSidebar"]::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: url('{image_url}');
                background-size: cover;
                background-position: center;
                opacity: 0.3;
                z-index: 0;
            }}
            [data-testid="stSidebar"]::after {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(255, 255, 255, 0.7);
                z-index: 1;
            }}
            [data-testid="stSidebar"] * {{
                position: relative;
                z-index: 2;
                color: black !important;
            }}
        </style>
    """, unsafe_allow_html=True)

def set_background(image_url):
    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url('{image_url}');
                background-size: cover;
                background-position: center;
            }}
            .overlay::before {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.7);
                z-index: 0;
            }}
        </style>
        <div class="overlay"></div>
    """, unsafe_allow_html=True)

def initialize_page(category):
    image_url = background_images.get(category, None)
    if image_url:
        set_background(image_url)
    set_sidebar_background(sidebar_image_url)
    st.title(f"{category} Analysis")

def show_overview_stats(health):
    initialize_page("Overview Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dataset Summary")
        total_indicators = health['Indicator Name'].nunique()
        total_records = len(health)
        years_covered = health['Year'].nunique()
        earliest_year = health['Year'].min()
        latest_year = health['Year'].max()
        
        st.metric("Total Indicators", total_indicators)
        st.metric("Total Records", total_records)
        st.metric("Years Covered", f"{earliest_year} to {latest_year}")
    
    with col2:
        st.subheader("Value Statistics")
        avg_value = health['Value'].mean()
        max_value_row = health.loc[health['Value'].idxmax()]
        min_value_row = health.loc[health['Value'].idxmin()]
        
        st.metric("Average Value", f"{avg_value:.2f}")
        st.metric("Highest Value", 
                 f"{max_value_row['Value']} ({max_value_row['Indicator Name']})")
        st.metric("Lowest Value", 
                 f"{min_value_row['Value']} ({min_value_row['Indicator Name']})")

    st.subheader("Full Dataset Preview")
    st.dataframe(health)

    st.subheader("Indicator Categories")
    for group in categories:
        with st.expander(group):
            st.markdown("• " + "<br>• ".join(categories[group]), unsafe_allow_html=True)

def show_trends_over_time(data, selected_indicators=None):
    initialize_page("Trends Over Time")
    st.subheader("Time Series Analysis of Health Indicators")
    
    try:
        # Show animated chart for all data if no specific indicators selected
        if not selected_indicators:
            st.info("Displaying trends for all available indicators")
            show_animated_line_chart(data)
        else:
            # Filter data for selected indicators
            filtered_data = data[data['Indicator Name'].isin(selected_indicators)]
            if not filtered_data.empty:
                show_animated_line_chart(filtered_data)
                for indicator in selected_indicators:
                    indicator_data = filtered_data[filtered_data['Indicator Name'] == indicator]
                    show_trend_chart(indicator_data, indicator, [indicator])
            else:
                st.warning("No data available for the selected indicators")
    except Exception as e:
        st.error(f"Error generating trends visualization: {str(e)}")
        
def show_demographic_and_population_insights(data):
    initialize_page("Demographic and Population Insights")
    st.subheader("Population Health Metrics")
    st.write("Analyze demographic trends and population health indicators.")

def show_health_expenditure_insights(data):
    initialize_page("Health Expenditure Insights")
    st.subheader("Healthcare Spending Analysis")
    st.write("Examine health expenditure patterns and funding allocations.")

def show_mortality_and_morbidity_trends(data):
    initialize_page("Mortality and Morbidity Trends")
    st.subheader("Mortality Patterns")
    st.write("Investigate mortality rates and causes of death across populations.")

def show_comparative_insights(data):
    initialize_page("Comparative Insights")
    st.subheader("Indicator Comparisons")
    st.write("Compare different health metrics side by side.")

def show_key_indicator_highlights(data):
    initialize_page("Key Indicator Highlights")
    st.subheader("Critical Health Metrics")
    st.write("Focus on key performance indicators and benchmarks.")

def show_maternal_child_piecharts(data):
    initialize_page("Maternal and Child Health")
    st.subheader("Maternal and Child Health Indicators")
    st.write("Analyze indicators related to maternal and child wellbeing.")

def show_infectious_diseases_piecharts(data):
    initialize_page("Infectious Diseases")
    st.subheader("Disease Prevalence and Prevention")
    st.write("Examine infectious disease trends and vaccination coverage.")

def show_nutrition_foodsecurity_piecharts(data):
    initialize_page("Nutrition and Food Security")
    st.subheader("Nutritional Health Metrics")
    st.write("Assess food security and nutritional status indicators.")

def show_expenditure_piecharts(data):
    initialize_page("Health Expenditure Insights")
    st.subheader("Health Expenditure Breakdown")
    st.write("View composition of health expenditures by category.")

def show_population_piecharts(data):
    initialize_page("Demographic and Population Insights")
    st.subheader("Population Demographics")
    st.write("Analyze population composition and characteristics.")

def show_mortality_piecharts(data):
    initialize_page("Mortality and Morbidity Trends")
    st.subheader("Mortality Composition")
    st.write("Breakdown of mortality by different causes.")

def show_category_data(filtered_data, category, selected_indicators):
    if selected_indicators:
        for indicator in selected_indicators:
            st.subheader(f"{indicator} Over Time")
            chart_data = filtered_data[filtered_data["Indicator Name"] == indicator]
            st.dataframe(chart_data[["Country Name", "Year", "Value"]])
    else:
        st.info("Select indicator(s) from the sidebar to view detailed data.")

def prepare_dashboard_data(health, category, selected_indicators, year_range, sort_order, keyword_filter):
    set_sidebar_background(sidebar_image_url)
    image_url = background_images.get(category, None)
    if image_url:
        set_background(image_url)
    
    st.title("Health Data Dashboard")
    start_year, end_year = year_range
    
    filtered = health[health['Year'].between(start_year, end_year)]
    ascending = True if sort_order == "Oldest to Newest" else False
    filtered = filtered.sort_values("Year", ascending=ascending)
    
    if keyword_filter != "All":
        keyword = keyword_filter.lower()
        filtered = filtered[filtered['Indicator Name'].str.lower().str.contains(keyword)]
    
    return filtered