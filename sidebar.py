import streamlit as st
from categories import categories

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
    }}

    /* SELECTION BOX STYLES - ORANGE WITH BLACK TEXT */
    div[data-baseweb="select"] [aria-selected="true"],
    div[data-baseweb="select"] [aria-selected="true"]:hover {{
        background-color: #FFA500 !important;  /* Orange background */
        color: #000000 !important;             /* Black text */
        font-weight: bold !important;
    }}

    /* Dropdown options */
    div[data-baseweb="select"] [role="option"] {{
        color: #000000 !important;
    }}

    /* Hover states for dropdown options */
    div[data-baseweb="select"] [role="option"]:hover {{
        background-color: #FFD699 !important;  /* Lighter orange */
        color: #000000 !important;
    }}

    /* Radio buttons and other selectors */
    div[data-baseweb="radio"] [aria-checked="true"] {{
        background-color: #FFA500 !important;
        color: #000000 !important;
        font-weight: bold !important;
    }}

    /* General text and labels */
    .st-emotion-cache-1v0mbdj,
    .stMarkdown, 
    .stText {{
        color: #000000 !important;
        font-weight: 500 !important;
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
    

def show_sidebar(health_data=None):
    """Combined sidebar with navigation and filters"""
    set_sidebar_background("https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Sidebar.png")
    
    # Navigation Section
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page", [
        "About",
        "Overview",
        "Data Explorer",
        "Forecasting",
        "Maternal and Child Health", 
        "Infectious Diseases",
        "Nutrition and Food Security",
        "Health Expenditures",
        "Population Health and Demographics",
        "Mortality Rates",
        "Comparative Insights",
        "Key Indicator Highlights"
    ], key="page_selector")
    
    # Initialize filters if they don't exist
    if 'current_filters' not in st.session_state:
        st.session_state.current_filters = {
            'year_range': (1960, 2023),
            'indicators': [],
            'keyword': "All",
            'category': "All",
            'sort_order': "Ascending"
        }
    
    # Always show filters (modified from original)
    st.sidebar.title("Data Filters")
    filters = create_data_filters(health_data)
    st.session_state.current_filters = filters
    
    return page

def create_data_filters(health_data):
    """Centralized filter controls with improved category handling"""
    filters = {}
    
    # 1. Category filter (using predefined categories)
    available_categories = ["All"] + list(categories.keys())
    filters['category'] = st.sidebar.selectbox(
        "Select Category", 
        available_categories,
        help="Filter data by indicator category",
        key="category_select"
    )
    
    # 2. Keyword filter
    keyword_options = ["All"] + sorted({
        kw for sublist in 
        [["child", "female", "male", "birth", "mortality"]] 
        for kw in sublist
    })
    
    filters['keyword'] = st.sidebar.selectbox(
        "Filter by keyword", 
        options=keyword_options,
        help="Narrow down indicators by common keywords",
        key="keyword_filter"
    )

    # 3. Indicator selection (from categories)
    if filters['category'] == "All":
        indicators = []
        for cat in categories.values():
            indicators.extend(cat)
        indicators = sorted(list(set(indicators)))  # Remove duplicates
    else:
        indicators = categories.get(filters['category'], [])
    
    if filters['keyword'] != "All":
        indicators = [ind for ind in indicators 
                     if filters['keyword'].lower() in ind.lower()]

    filters['indicators'] = st.sidebar.multiselect(
        "Select Indicators", 
        options=indicators,
        default=indicators[:3] if len(indicators) > 3 else indicators,
        key="indicator_select"
    )

    # 4. Year range (from actual data)
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
        filters['year_range'] = (1960, 2023)  # Default fallback

    # 5. Sort order
    filters['sort_order'] = st.sidebar.radio(
        "Sort Order",
        ["Ascending", "Descending"],
        horizontal=True,
        key="sort_order"
    )

    return filters