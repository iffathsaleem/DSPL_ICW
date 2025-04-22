import streamlit as st

def set_sidebar_background(image_url):
    st.markdown(f"""
        <style>
        /* Apply background image and overlay to the entire sidebar */
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
            opacity: 0.3; /* Slight opacity to the background */
            z-index: 0;
        }}

        /* White overlay with 70% opacity over the image */
        [data-testid="stSidebar"]::after {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 255, 255, 0.7); /* 70% white overlay */
            z-index: 1;
        }}

        /* Ensure text is above the background and white overlay */
        [data-testid="stSidebar"] * {{
            position: relative;
            z-index: 2;
            color: black !important; /* Make all sidebar text black */
        }}

        /* Adding margin-top to avoid overlap with other components */
        .sidebar .css-1d391kg {{
            margin-top: 20px;
        }}
        .sidebar .css-1d391kg .css-1v0mbdj {{
            padding-top: 10px;
        }}
        </style>
    """, unsafe_allow_html=True)

background_image_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/png-transparent-medicine-health-care-logo-health-love-text-heart-thumbnail.png"

if 'background_image_set' not in st.session_state:
    set_sidebar_background(background_image_url)
    st.session_state.background_image_set = True  

def sidebar_filters(df):
    st.sidebar.title("Health Data Filters")

    # Define the categories and their associated indicators
    categories = {
        "Maternal and Child Health": [
            "Adolescent fertility rate (births per 1,000 women ages 15-19)",
            "Birth rate, crude (per 1,000 people)",
            "Births attended by skilled health staff (% of total)",
            "Low-birthweight babies (% of births)",
            "Maternal mortality ratio (modeled estimate, per 100,000 live births)",
            "Infant mortality rate (per 1,000 live births)",
            "Exclusive breastfeeding (% of children under 6 months)"
        ],
        "Infectious Diseases": [
            "Adults (ages 15+) and children (ages 0-14) newly infected with HIV",
            "Incidence of HIV, all (per 1,000 uninfected population)",
            "Incidence of tuberculosis (per 100,000 people)",
            "Incidence of malaria (per 1,000 population at risk)",
            "Immunization, DPT (% of children ages 12-23 months)"
        ],
        "Nutrition and Food Security": [
            "Prevalence of anemia among children (% of children ages 6-59 months)",
            "Prevalence of stunting, height for age (% of children under 5)",
            "Prevalence of wasting, weight for height (% of children under 5)",
            "Prevalence of underweight, weight for age (% of children under 5)",
            "Prevalence of moderate or severe food insecurity in the population (%)"
        ],
        "Health Expenditures": [
            "Current health expenditure (% of GDP)",
            "Current health expenditure per capita (current US$)",
            "Domestic general government health expenditure (% of GDP)",
            "Domestic private health expenditure (% of current health expenditure)",
            "Out-of-pocket expenditure (% of current health expenditure)"
        ],
        "Population Health and Demographics": [
            "Life expectancy at birth, female (years)",
            "Life expectancy at birth, male (years)",
            "Population growth (annual %)",
            "Population, female",
            "Population, male",
            "Women who were first married by age 18 (% of women ages 20-24)"
        ],
        "Mortality Rates": [
            "Mortality rate, adult, female (per 1,000 female adults)",
            "Mortality rate, infant (per 1,000 live births)",
            "Mortality rate attributed to household and ambient air pollution, age-standardized (per 100,000 population)",
            "Suicide mortality rate (per 100,000 population)"
        ]
    }

    # Sidebar Filters
    category = st.sidebar.selectbox("Select Category", list(categories.keys()))
    keyword_filter = st.sidebar.selectbox("Filter indicators by keyword", ["All", "kids", "female", "male"])

    # Filter indicators based on selected category and keyword
    indicators = categories[category]
    if keyword_filter != "All":
        indicators = [i for i in indicators if keyword_filter.lower() in i.lower()]

    selected_indicators = st.sidebar.multiselect("Select Indicator(s)", indicators)

    # Handle year selection
    years = sorted(df['Year'].dropna().unique())
    year_range = st.sidebar.slider("Select Year Range", int(min(years)), int(max(years)),
                                   (int(min(years)), int(max(years))))

    # Handle year sorting
    sort_order = st.sidebar.radio("Sort Year", ["Oldest to Newest", "Newest to Oldest"])

    return category, selected_indicators, year_range, sort_order, keyword_filter

def show_sidebar():
    st.sidebar.title("Navigation")
    # Add all the sections in the sidebar
    page = st.sidebar.radio("Select a page", [
        "About", 
        "Overview Dashboard", 
        "Trends Over Time", 
        "Demographic Insights", 
        "Expenditure Analysis", 
        "Mortality & Morbidity", 
        "Comparative Insights", 
        "Key Indicator Highlights"
    ])
    return page
