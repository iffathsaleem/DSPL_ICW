def sidebar_filters(df):
    st.sidebar.title("Health Data Filters")

    # View selector
    view = st.sidebar.radio("Select View", ["About", "Indicators"])

    # Category selector (only show if Indicators selected)
    category = None
    if view == "Indicators":
        categories = {
            "Fertility & Birth": [
                "Fertility rate, total (births per woman)",
                "Birth rate, crude (per 1,000 people)",
                "Adolescent fertility rate (births per 1,000 women ages 15-19)",
                "Teenage mothers (% of women ages 15-19 who have had children or are currently pregnant)",
            ],
            "Mortality & Life Expectancy": [
                "Life expectancy at birth, total (years)",
                "Mortality rate, infant (per 1,000 live births)",
                "Suicide mortality rate (per 100,000 population)",
                "Number of under-five deaths",
            ],
            "Disease & Infection": [
                "Incidence of HIV, all (per 1,000 uninfected population)",
                "Incidence of tuberculosis (per 100,000 people)",
                "Children with fever receiving antimalarial drugs",
                "Prevalence of anemia among children",
            ],
            "Healthcare Access & Spending": [
                "Births attended by skilled health staff (% of total)",
                "Current health expenditure (% of GDP)",
                "Number of surgical procedures (per 100,000 population)",
                "People using at least basic sanitation services (% of population)",
            ]
        }
        category = st.sidebar.selectbox("Indicator Category", list(categories.keys()))

        # Indicator selector
        indicators = categories[category]
        selected_indicators = st.sidebar.multiselect("Select Indicator(s)", indicators)

        # Year filters
        sort_order = st.sidebar.radio("Year Order", ["Oldest to Newest", "Newest to Oldest"])
        min_year = int(df["Year"].min())
        max_year = int(df["Year"].max())
        year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

        return view, category, selected_indicators, year_range, sort_order
    else:
        return view, None, None, None, None