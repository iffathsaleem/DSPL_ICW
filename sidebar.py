import streamlit as st
from dashboard import set_sidebar_background
from categories import categories

def show_sidebar():
    """Display the sidebar navigation with background styling"""
    background_image_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Sidebar.png"
    set_sidebar_background(background_image_url)

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
    """Display data filters in the sidebar and return filter selections"""
    st.sidebar.title("Data Filters")
    
    # Category selection based on predefined categories
    available_categories = list(categories.keys())
    category = st.sidebar.selectbox(
        "Select Category", 
        available_categories,
        help="Filter data by indicator category"
    )
    
    # Keyword filter with simplified options
    keyword_filter = st.sidebar.selectbox(
        "Filter by keyword", 
        ["All", "child", "female", "male", "birth", "mortality"],
        help="Narrow down indicators by common keywords"
    )

    # Get indicators for selected category
    indicators = categories.get(category, [])
    
    # Apply keyword filter if not "All"
    if keyword_filter != "All":
        indicators = [ind for ind in indicators if keyword_filter.lower() in ind.lower()]

    # Indicator selection with smart defaults
    selected_indicators = st.sidebar.multiselect(
        "Select Indicators", 
        options=indicators,
        default=indicators[:3] if len(indicators) > 3 else indicators,
        help="Select up to 5 indicators to analyze"
    )

    # Year range slider (fixed the unclosed parenthesis issue)
    years = sorted(health_data['Year'].dropna().unique())
    year_range = st.sidebar.slider(
        "Year Range", 
        min_value=int(min(years)), 
        max_value=int(max(years)),
        value=(int(min(years)), int(max(years))),  # Fixed this line
        help="Select the time period to analyze"
    )
    
    # Sort order radio buttons
    sort_order = st.sidebar.radio(
        "Sort Order", 
        options=["Oldest to Newest", "Newest to Oldest"],
        horizontal=True,
        help="Sort data chronologically or reverse chronologically"
    )

    return category, selected_indicators, year_range, sort_order, keyword_filter