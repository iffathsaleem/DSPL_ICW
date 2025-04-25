import streamlit as st
from dashboard import set_sidebar_background

def show_sidebar():
    background_image_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Sidebar.png"
    set_sidebar_background(background_image_url)

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page", [
        "About", 
        "Overview Dashboard", 
        "Trends Over Time",
        "Demographic and Population Insights",
        "Health Expenditure Insights", 
        "Mortality and Morbidity Trends", 
        "Comparative Insights", 
        "Key Indicator Highlights",
        "Maternal and Child Health",
        "Infectious Diseases",
        "Nutrition and Food Security"
    ])
    return page

def sidebar_filters(health):
    st.sidebar.title("Data Filters")
    
    if 'Category' in health.columns:
        available_categories = health['Category'].unique()
        category = st.sidebar.selectbox("Select Category", available_categories)
    else:
        category = st.sidebar.selectbox("Select Category", ["Overview"])
    
    keyword_filter = st.sidebar.selectbox(
        "Filter by keyword", 
        ["All", "kids", "female", "male", "child", "birth", "mortality"]
    )

    if 'Category' in health.columns:
        indicators = health[health['Category'] == category]['Indicator Name'].unique()
    else:
        indicators = []
        
    if keyword_filter != "All":
        indicators = [i for i in indicators if keyword_filter.lower() in i.lower()]

    selected_indicators = st.sidebar.multiselect(
        "Select Indicators", 
        indicators,
        max_selections=5
    )

    years = sorted(health['Year'].dropna().unique())
    year_range = st.sidebar.slider(
        "Year Range", 
        int(min(years)), 
        int(max(years)),
        (int(min(years)), int(max(years)))
    )
    
    sort_order = st.sidebar.radio(
        "Sort Order", 
        ["Oldest to Newest", "Newest to Oldest"],
        horizontal=True
    )

    return category, selected_indicators, year_range, sort_order, keyword_filter