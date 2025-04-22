import streamlit as st

def sidebar_filters(df):
    st.sidebar.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
                          url('https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/png-transparent-medicine-health-care-logo-health-love-text-heart-thumbnail.png');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    /* Ensure white text for all sidebar elements */
    .stSelectbox div[data-baseweb="select"],
    .stMultiSelect div[data-baseweb="select"],
    .stSlider,
    .stRadio,
    .css-1cpxqw2, .css-1v0mbdj, .css-1r6slb0,
    label, .css-10trblm, .css-qrbaxs, .css-16huue1 {
        color: white !important;
    }

    /* Fix multiselect selected pills */
    .css-1n76uvr, .css-1p3m7a8 {
        background-color: #444 !important;
        color: white !important;
        border: 1px solid white !important;
    }

    /* Select box internal text (selected value) */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        color: white !important;
    }

    /* Dropdown options text */
    .css-1wa3eu0-option {
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

    # Sidebar filters
    category = st.sidebar.selectbox("Select Category", list(categories.keys()))
    keyword_filter = st.sidebar.selectbox("Filter indicators by keyword", ["All", "kids", "female", "male"])

    # Filter indicators based on category and keyword
    indicators = categories[category]
    if keyword_filter != "All":
        indicators = [i for i in indicators if keyword_filter.lower() in i.lower()]

    selected_indicators = st.sidebar.multiselect("Select Indicator(s)", indicators)

    # Year selection
    years = sorted(df['Year'].dropna().unique())
    year_range = st.sidebar.slider(
        "Select Year Range",
        int(min(years)), int(max(years)),
        (int(min(years)), int(max(years)))
    )

    # Sorting
    sort_order = st.sidebar.radio("Sort Year", ["Oldest to Newest", "Newest to Oldest"])

    return category, selected_indicators, year_range, sort_order, keyword_filter


def filter_data_by_keywords(df, keyword):
    """Filters data based on keyword search in the 'Indicator' column."""
    return df[df['Indicator'].str.contains(keyword, case=False, na=False)]


def get_selected_category_image(category):
    """Returns the background image URL based on the selected category."""
    category_images = {
        "Maternal and Child Health": "https://github.com/iffathsaleem/DSPL_ICW/blob/main/Images/Mother%20smiling%20at%20the%20child%202.jpg",
        "Infectious Diseases": "https://github.com/iffathsaleem/DSPL_ICW/blob/main/Images/picture2.jpg",
        "Nutrition and Food Security": "https://github.com/iffathsaleem/DSPL_ICW/blob/main/Images/image_21e6d3c403.jpg",
        "Health Expenditures": "https://github.com/iffathsaleem/DSPL_ICW/blob/main/Images/health.jpg",
        "Population Health and Demographics": "https://github.com/iffathsaleem/DSPL_ICW/blob/main/Images/Web-Banner-Health-o4f17s40uhwhne99pga2mrovntcwm1s7r06v5rb0gc.jpg",
        "Mortality Rates": "https://github.com/iffathsaleem/DSPL_ICW/blob/main/Images/images.jpeg"
    }
    return category_images.get(category, "")
