import streamlit as st

def sidebar_filters(df):
    st.sidebar.title("Health Data Filters")

    # View selector
    view = st.sidebar.radio("Select View", ["Dashboard", "About"])

    # Categories and indicators
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

    # Category selector
    category = st.sidebar.selectbox("Select Category", list(categories.keys()))
    indicators = categories[category]
    selected_indicators = st.sidebar.multiselect("Select Indicators", indicators, default=indicators[:1])

    # Year range selector
    years = sorted(df['Year'].unique())
    sort_order = st.sidebar.radio("Sort Year", ["Oldest to Newest", "Newest to Oldest"])

    if sort_order == "Newest to Oldest":
        years = sorted(years, reverse=True)

    year_range = st.sidebar.slider("Select Year Range", int(min(years)), int(max(years)), (int(min(years)), int(max(years))))

    return view, category, selected_indicators, year_range, sort_order
