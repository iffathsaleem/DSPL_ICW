import streamlit as st
from categories import categories

# Background images for each category
SECTION_BACKGROUNDS = {
    "Mortality Rates Analysis": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Mortality%20Rates.jpeg",
    "Maternal and Child Health Analysis": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Maternal%20and%20Child%20Health.jpg",
    "Infectious Diseases Analysis": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Infectious%20Diseases.jpg",
    "Health Expenditure Analysis": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Health%20Expenditures.jpg",
    "Healthcare Infrastructure and Services Analysis": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Healthcare%20Infrastructure%20and%20Services.jpg",
    "Water, Sanitation and Hygiene Analysis": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Water%2C%20Sanitation%2C%20and%20Hygiene.png",
    "Non-communicable Diseases and Risk Factors Analysis": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Non-communicable%20Diseases%20and%20Risk%20Factors.jpg",
    "Nutrition and Food Security Analysis": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Nutrition%20and%20Food%20Security.jpg",
    "Demographic Indicators Analysis": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Demographic%20Insights.jpg",
    "Reproductive Health Analysis": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Reproductive%20Health.jpg",
    "Civil Registration Analysis": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Civil%20Registration.jpg",
    "Injury and External Causes Analysis": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Injury%20and%20External%20Causes.jpg"
}

def set_section_background(category):
    image_url = SECTION_BACKGROUNDS.get(category)
    if image_url:
        st.markdown(f"""
        <style>
        /* Main app background with dark overlay */
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                        url('{image_url}') center/cover no-repeat fixed;
        }}
        
        /* Main content area - semi-transparent dark container */
        .main .block-container {{
            background-color: rgba(30, 30, 30, 0.85) !important;
            border-radius: 10px;
            padding: 2rem;
            margin-top: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
        }}
        
        /* All text white by default */
        .main .block-container * {{
            color: #ffffff !important;
        }}
        
        /* Headers with white color */
        .main .block-container h1,
        .main .block-container h2,
        .main .block-container h3 {{
            color: #ffffff !important;
            border-bottom: 1px solid #555;
            padding-bottom: 0.5rem;
        }}
        
        /* Widget styling */
        .stTextInput input, 
        .stSelectbox select,
        .stSlider .st-c7,
        .stNumberInput input {{
            background-color: rgba(45, 45, 45, 0.9) !important;
            color: white !important;
            border: 1px solid #555 !important;
        }}
        
        /* Buttons */
        .stButton>button {{
            background-color: #1976d2 !important;
            color: white !important;
            border: none !important;
        }}
        
        /* Dataframes */
        .stDataFrame {{
            background-color: rgba(45, 45, 45, 0.9) !important;
        }}
        
        /* Markdown tables */
        .main .block-container table {{
            background-color: rgba(45, 45, 45, 0.9) !important;
        }}
        
        /* Links */
        .main .block-container a {{
            color: #4fc3f7 !important;
        }}
        </style>
        """, unsafe_allow_html=True)
        
def set_sidebar_background():
    sidebar_image_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Sidebar.png"
    st.markdown(f"""
    <style>
    /* Main sidebar container with background image */
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
        background-image: url('{sidebar_image_url}');
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
        background-color: rgba(0, 0, 0, 0.7);
        z-index: 1;
    }}

    [data-testid="stSidebar"] > * {{
        position: relative;
        z-index: 2;
        color: #ffffff !important;
    }}
    
    /* Remove white boxes behind filter labels */
    [data-testid="stSidebar"] div[data-baseweb="base-input"] > div,
    [data-testid="stSidebar"] div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stRadio label {{
        background-color: transparent !important;
    }}
    
    /* Text elements - white with better contrast */
    [data-testid="stSidebar"] * {{
        color: #ffffff !important;
    }}
    
    /* Input fields styling */
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] .stSelectbox select,
    [data-testid="stSidebar"] .stNumberInput input {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #000000 !important;
        border: 1px solid #d0d0d0 !important;
    }}
    
    /* Section headers */
    [data-testid="stSidebar"] h1 {{
        background-color: transparent !important;
        font-size: 1.25rem;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        padding-bottom: 0.25rem;
        color: #ffffff !important;
    }}
    
    /* Proper spacing between filters */
    [data-testid="stSidebar"] .stSlider,
    [data-testid="stSidebar"] .stMultiSelect,
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stRadio {{
        margin-bottom: 1.25rem !important;
        padding: 0.25rem 0 !important;
    }}
    
    /* Remove extra padding in multiselect */
    [data-testid="stSidebar"] .stMultiSelect > div > div {{
        padding-top: 0 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

def show_sidebar(health_data=None):
    set_sidebar_background()
    
    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Go to", [
            "About",
            "Overview",
            "Data Analysis",
            "Comparative Insights"
        ], key="nav_radio")

        if page == "Data Analysis":
            st.markdown("---")
            page = st.selectbox(
                "Select Category",
                [f"{cat} Analysis" for cat in categories.keys()],
                key="category_select"
            )

        st.markdown("---")
        st.title("Data Filters")
        
        # Initialize filters dict
        filters = {}
        
        # Year range filter
        years = (1960, 2023) if health_data is None else (
            int(health_data['Year'].min()), int(health_data['Year'].max()))
        filters['year_range'] = st.slider(
            "Year Range",
            min_value=years[0],
            max_value=years[1],
            value=years,
            key="year_filter"
        )
        
        # Category filter
        selected_categories = st.multiselect(
            "Categories",
            options=list(categories.keys()),
            default=list(categories.keys())[:1],
            key="category_filter"
        )
        
        # Keyword filter
        keywords = st.multiselect(
            "Filter by keywords",
            options=["child", "female", "male", "birth", "mortality"],
            key="keyword_filter"
        )
        
        # Sort order
        sort_order = st.radio(
            "Sort Order",
            ["Ascending", "Descending"],
            index=0,
            horizontal=True,
            key="sort_filter"
        )

    return page, filters