import streamlit as st
import pandas as pd
import plotly.express as px

# Categories and their indicator mappings
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

# Background image mapping for categories
background_images = {
    "Maternal and Child Health": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Mother%20smiling%20at%20the%20child%202.jpg",
    "Infectious Diseases": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/picture2.jpg",
    "Nutrition and Food Security": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/image_21e6d3c403.jpg",
    "Health Expenditures": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/health.jpg",
    "Population Health and Demographics": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Web-Banner-Health-o4f17s40uhwhne99pga2mrovntcwm1s7r06v5rb0gc.jpg",
    "Mortality Rates": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/images.jpeg"
}

# Set background image for the sidebar
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
        </style>
    """, unsafe_allow_html=True)

def set_background(image_url):
    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url('{image_url}');
                background-size: cover;
                background-position: center;
            }}
            .overlay::before {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.7);
                z-index: 0;
            }}
        </style>
        <div class="overlay"></div>
    """, unsafe_allow_html=True)

# Show dashboard with selected category and filters
def show_dashboard(df, category, selected_indicators, year_range, sort_order, keyword_filter):
    if 'sidebar_background_set' not in st.session_state:
        image_url = background_images.get(category, None)
        if image_url:
            set_sidebar_background(image_url)
        st.session_state.sidebar_background_set = True  # Flag to ensure it is set only once
    
    # Set the main app background image
    if 'background_image_set' not in st.session_state:
        image_url = background_images.get(category, None)
        if image_url:
            set_background(image_url)
        st.session_state.background_image_set = True 
    st.title("Health Data Dashboard")
    start_year, end_year = year_range

    # Filter by year
    filtered = df[df['Year'].between(start_year, end_year)]

    # Sort order
    ascending = True if sort_order == "Oldest to Newest" else False
    filtered = filtered.sort_values("Year", ascending=ascending)

    # Filter indicators by keyword
    if keyword_filter != "All":
        keyword = keyword_filter.lower()
        filtered = filtered[filtered['Indicator Name'].str.lower().str.contains(keyword)]

    # Show pie charts per year for category
    st.subheader(f"Category Overview: {category}")
    category_indicators = categories[category]
    category_data = filtered[filtered["Indicator Name"].isin(category_indicators)]

    for year in sorted(category_data['Year'].unique()):
        yearly_data = category_data[category_data['Year'] == year]
        pie_data = yearly_data.groupby("Indicator Name")["Value"].sum().reset_index()
        if not pie_data.empty:
            fig = px.pie(pie_data, names="Indicator Name", values="Value", title=f"{category} Distribution - {year}")
            st.plotly_chart(fig, use_container_width=True)

    # Line charts and data for selected indicators
    if selected_indicators:
        for indicator in selected_indicators:
            st.subheader(f"{indicator} Over Time")
            chart_data = filtered[filtered["Indicator Name"] == indicator]

            fig_line = px.line(chart_data, x="Year", y="Value", color="Country Name", title=indicator)
            st.plotly_chart(fig_line)

            st.dataframe(chart_data[["Country Name", "Year", "Value"]])
    else:
        st.info("Select indicator(s) from the sidebar to view charts and data.")
