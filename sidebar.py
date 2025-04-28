import streamlit as st
from categories import categories  # Ensure categories is correctly imported

# Function to set the background for the sidebar
def set_sidebar_background(image_url):
    st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{
        position: relative;
    }}
    
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

    [data-testid="stSidebar"] > * {{
        position: relative;
        z-index: 2;
        color: #000000 !important;  /* Ensure all text is black */
    }}

    /* Make sure all text elements are black */
    .st-emotion-cache-10trblm, 
    .st-emotion-cache-1v0mbdj,
    .stMarkdown, 
    .stText,
    .stSelectbox label,
    .stRadio label,
    .stSlider label,
    .stMultiSelect label {{
        color: #000000 !important;
    }}

    /* Input fields */
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #000000 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# Function to show the sidebar with filters
def show_sidebar(health_data=None):
    """Combined sidebar with navigation and filters"""
    set_sidebar_background("https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Sidebar.png")
    
    # Navigation Section
    st.sidebar.title("Navigation")
    
    # Main sections (About, Overview, Data Analysis)
    page = st.sidebar.radio("Go to", [
        "About",
        "Overview",
        "Data Analysis",
        "Comparative Insights"
    ], key="main_page_selector")

    # If Data Analysis is selected, show category selector
    if page == "Data Analysis":
        page = st.sidebar.selectbox(
            "Select Category",
            [
                "Mortality Rates",
                "Maternal and Child Health",
                "Infectious Diseases",
                "Health Expenditure",
                "Healthcare Infrastructure and Services",
                "Water, Sanitation, and Hygiene",
                "Non-communicable Diseases and Risk Factors",
                "Nutrition and Food Security",
                "Demographic Indicators",
                "Reproductive Health",
                "Civil Registration",
                "Injury and External Causes"
                
            ],
            key="category_selector"
        )
    
    # Initialize filters if they don't exist
    if 'current_filters' not in st.session_state:
        st.session_state.current_filters = {
            'year_range': (1960, 2023),
            'indicators': [],
            'keyword': "All",
            'category': "All",
            'sort_order': "Ascending"
        }
    
    # Always show filters
    st.sidebar.title("Data Filters")
    filters = create_data_filters(health_data)
    st.session_state.current_filters = filters
    
    return page

# Function to create data filters (categories, keywords, indicators, etc.)
def create_data_filters(health_data):
    """Centralized filter controls with improved category handling"""
    filters = {}
    
    # 1. Category filter
    available_categories = list(categories.keys())
    filters['categories'] = st.sidebar.multiselect(
        "Select Categories", 
        available_categories,
        default=available_categories[:1],
        help="Filter data by indicator categories",
        key="category_select"
    )
    
    # 2. Keyword filter
    keyword_options = ["child", "female", "male", "birth", "mortality", "health", "population"]
    filters['keywords'] = st.sidebar.multiselect(
        "Filter by keywords", 
        options=keyword_options,
        default=[],
        help="Narrow down indicators by keywords",
        key="keyword_filter"
    )

    # 3. Indicator selection
    indicators = []
    if not filters['categories']:
        for cat in categories.values():
            indicators.extend(cat)
    else:
        for category in filters['categories']:
            indicators.extend(categories.get(category, []))
    
    if filters['keywords']:
        indicators = [ind for ind in indicators 
                     if any(kw.lower() in ind.lower() for kw in filters['keywords'])]

    indicators = sorted(list(set(indicators)))
    
    filters['indicators'] = st.sidebar.multiselect(
        "Select Indicators", 
        options=indicators,
        default=indicators[:3] if len(indicators) > 3 else indicators,
        key="indicator_select"
    )

    # 4. Year range
    if health_data is not None:
        years = sorted(health_data['Year'].unique())
        filters['year_range'] = st.sidebar.slider(
            "Year Range",
            min_value=int(min(years)),
            max_value=int(max(years)),
            value=(int(min(years)), int(max(years))),
            key="year_slider"
        )
    else:
        filters['year_range'] = (1960, 2023)  

    # 5. Sort order - only show this once
    if 'sort_order' not in st.session_state:
        filters['sort_order'] = st.sidebar.radio(
            "Sort Order",
            ["Ascending", "Descending"],
            horizontal=True,
            key="sort_order"
        )
    else:
        filters['sort_order'] = st.session_state.sort_order

    return filters