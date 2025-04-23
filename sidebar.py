import streamlit as st
from categories import categories


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

background_image_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Sidebar.png"

if 'background_image_set' not in st.session_state:
    set_sidebar_background(background_image_url)
    st.session_state.background_image_set = True  

def sidebar_filters(health):
    st.sidebar.title("Health Data Filters")

    category = st.sidebar.selectbox("Select Category", list(categories.keys()))
    keyword_filter = st.sidebar.selectbox("Filter indicators by keyword", ["All", "kids", "female", "male"])

    indicators = categories[category]
    if keyword_filter != "All":
        indicators = [i for i in indicators if keyword_filter.lower() in i.lower()]

    selected_indicators = st.sidebar.multiselect("Select Indicator(s)", indicators)

    years = sorted(health['Year'].dropna().unique())
    year_range = st.sidebar.slider("Select Year Range", int(min(years)), int(max(years)),
                                   (int(min(years)), int(max(years))))

    sort_order = st.sidebar.radio("Sort Year", ["Oldest to Newest", "Newest to Oldest"])

    return category, selected_indicators, year_range, sort_order, keyword_filter

def show_sidebar():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page", [
        "About", 
        "Overview Dashboard", 
        "Trends Over Time", 
        "Demographic Insights", 
        "Expenditure Analysis", 
        "Mortality & Morbidity", 
        "Comparative Insights", 
        "Key Indicator Highlights",
        "Maternal and Child Health",
        "Infectious Diseases",
        "Nutrition and Food Security",
        "Health Expenditures",
        "Population Health and Demographics",
        "Mortality Rates"
    ])
    return page
