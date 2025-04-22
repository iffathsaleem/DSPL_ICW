import streamlit as st

def sidebar_filters(df):
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
    
    # Sidebar filters for category, indicators, year range, etc.
    category = st.sidebar.selectbox("Select Category", list(categories.keys()))
    selected_indicators = st.sidebar.multiselect("Select Indicators", categories[category], default=categories[category])
    year_range = st.sidebar.slider("Select Year Range", int(df['Year'].min()), int(df['Year'].max()), (int(df['Year'].min()), int(df['Year'].max())))
    sort_order = st.sidebar.radio("Sort Order", ["Ascending", "Descending"])
    keyword_filter = st.sidebar.text_input("Filter by Keyword (e.g. 'female', 'kids')")

    return category, selected_indicators, year_range, sort_order, keyword_filter
