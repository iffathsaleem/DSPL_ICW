import streamlit as st
import pandas as pd
from categories import categories, map_category
from visualizations import show_trend_chart

# Background image configuration (renamed Overview)
background_images = {
    "About": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/About.jpg",
    "Overview": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Overview.jpg",
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
    st.title(f"{category}")

import plotly.express as px

def show_overview(health_data):
    initialize_page("Overview")
    
    # Basic statistics
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dataset Summary")
        st.metric("Total Indicators", health_data['Indicator Name'].nunique())
        st.metric("Years Covered", f"{health_data['Year'].min()} to {health_data['Year'].max()}")
    
    with col2:
        st.subheader("Value Statistics")
        st.metric("Average Value", f"{health_data['Value'].mean():.2f}")
        st.metric("Data Points", len(health_data))

    # Animated visualization
    st.subheader("Animated Trends for All Indicators")
    
    try:
        # Create a sample of data if dataset is too large
        if len(health_data) > 1000:
            sample_data = health_data.sample(1000)
            st.warning("Showing random sample of 1000 points for better performance")
        else:
            sample_data = health_data
            
        fig = px.scatter(
            sample_data.sort_values('Year'),
            x='Year',
            y='Value',
            color='Indicator Name',
            animation_frame='Year',
            title='Health Indicators Over Time',
            labels={'Value': 'Value', 'Year': 'Year'},
            height=600
        )
        
        fig.update_layout(
            xaxis_range=[sample_data['Year'].min()-1, sample_data['Year'].max()+1],
            yaxis_range=[sample_data['Value'].min()*0.9, sample_data['Value'].max()*1.1],
            transition={'duration': 300}
        )
        
        # Add play button
        fig.update_layout(
            updatemenus=[{
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 500, "redraw": True},
                                    "fromcurrent": True, "transition": {"duration": 300}}],
                        "label": "Play",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Animation failed: {str(e)}")
        st.write("Showing static visualization instead")
        st.dataframe(health_data)

def show_demographic_and_population_insights(data):
    show_category_analysis(data, "Demographic and Population Insights")

def show_health_expenditure_insights(data):
    show_category_analysis(data, "Health Expenditure Insights")

def show_mortality_and_morbidity_trends(data):
    show_category_analysis(data, "Mortality and Morbidity Trends")

def show_comparative_insights(data):
    show_category_analysis(data, "Comparative Insights")

def show_key_indicator_highlights(data):
    show_category_analysis(data, "Key Indicator Highlights")

def show_maternal_child_piecharts(data):
    show_category_analysis(data, "Maternal and Child Health")

def show_infectious_diseases_piecharts(data):
    show_category_analysis(data, "Infectious Diseases")

def show_nutrition_foodsecurity_piecharts(data):
    show_category_analysis(data, "Nutrition and Food Security")

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

def show_category_data(filtered_data, category, selected_indicators):
    if selected_indicators:
        for indicator in selected_indicators:
            st.subheader(f"{indicator} Over Time")
            chart_data = filtered_data[filtered_data["Indicator Name"] == indicator]
            st.dataframe(chart_data[["Country Name", "Year", "Value"]])
    else:
        st.info("Select indicator(s) from the sidebar to view detailed data.")