import streamlit as st
from dashboard import set_sidebar_background
from categories import categories

def show_sidebar():
    set_sidebar_background("https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Sidebar.png")
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page", [
        "About",
        "Overview",
        "Maternal and Child Health", 
        "Infectious Diseases",
        "Nutrition and Food Security",
        "Health Expenditures",
        "Population Health and Demographics",
        "Mortality Rates",
        "Comparative Insights",
        "Key Indicator Highlights"
    ])
    return page

def sidebar_filters(health_data):
    st.sidebar.title("Data Filters")
    available_categories = list(categories.keys())
    
    category = st.sidebar.selectbox(
        "Select Category", 
        available_categories,
        help="Filter data by indicator category"
    )
    
    keyword_filter = st.sidebar.selectbox(
        "Filter by keyword", 
        ["All", "child", "female", "male", "birth", "mortality"],
        help="Narrow down indicators by common keywords"
    )

    indicators = categories.get(category, [])
    if keyword_filter != "All":
        indicators = [ind for ind in indicators if keyword_filter.lower() in ind.lower()]

    selected_indicators = st.sidebar.multiselect(
        "Select Indicators", 
        options=indicators,
        default=indicators[:3] if len(indicators) > 3 else indicators
    )

    years = sorted(health_data['Year'].unique())
    year_range = st.sidebar.slider(
        "Year Range",
        min_value=int(min(years)),
        max_value=int(max(years)),
        value=(int(min(years)), int(max(years))))
    
    sort_order = st.sidebar.radio(
        "Sort Order",
        ["Oldest to Newest", "Newest to Oldest"],
        horizontal=True
    )

    return category, selected_indicators, year_range, sort_order, keyword_filter