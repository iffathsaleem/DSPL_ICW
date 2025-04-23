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

# Sidebar image URL
sidebar_image_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/png-transparent-medicine-health-care-logo-health-love-text-heart-thumbnail.png"

# Set background image for the sidebar
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

# Set main background for the app
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
    set_sidebar_background(sidebar_image_url)

    image_url = background_images.get(category, None)
    if image_url:
        set_background(image_url)

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

# Overview Dashboard
def show_overview_dashboard(df):
    st.title("Overview Dashboard")

    # Basic Stats
    total_indicators = df['Indicator Name'].nunique()
    total_records = len(df)
    years_covered = df['Year'].nunique()
    earliest_year = df['Year'].min()
    latest_year = df['Year'].max()
    avg_value = df['Value'].mean()

    most_frequent_indicator = df['Indicator Name'].value_counts().idxmax()
    top_avg_indicator = df.groupby('Indicator Name')['Value'].mean().idxmax()
    max_value_row = df.loc[df['Value'].idxmax()]
    min_value_row = df.loc[df['Value'].idxmin()]

    st.subheader("Key Statistics")
    st.markdown(f"- Total Records: {total_records}")
    st.markdown(f"- Number of Unique Indicators: {total_indicators}")
    st.markdown(f"- Years Covered: {years_covered} ({earliest_year} to {latest_year})")
    st.markdown(f"- Average Value Across All Indicators: {avg_value:.2f}")
    st.markdown(f"- Most Frequent Indicator: {most_frequent_indicator}")
    st.markdown(f"- Top Indicator by Average Value: {top_avg_indicator}")
    st.markdown(f"- Highest Value: {max_value_row['Value']} ({max_value_row['Indicator Name']} in {max_value_row['Year']})")
    st.markdown(f"- Lowest Value: {min_value_row['Value']} ({min_value_row['Indicator Name']} in {min_value_row['Year']})")

    # CSV Data Preview
    st.subheader("Full Dataset")
    st.dataframe(df)

    # Indicator Groups
    st.subheader("Indicator Groupings")
    for group, indicators in categories.items():
        st.markdown(f"**{group}**")
        st.markdown("• " + "<br>• ".join(indicators), unsafe_allow_html=True)

    # Bar Chart of Indicator Frequency (using Indicator Code)
    st.subheader("Indicator Frequency by Code")
    freq_df = df['Indicator_Code'].value_counts().reset_index()
    freq_df.columns = ['Indicator_Code', 'Count']
    fig_bar = px.bar(freq_df, x='Indicator_Code', y='Count', title="Frequency of Each Indicator (Code)")
    st.plotly_chart(fig_bar)

    # Code-to-Name Legend Table
    st.markdown("**Indicator Code Reference Table**")
    code_name_df = df[['Indicator_Code', 'Indicator Name']].drop_duplicates().sort_values('Indicator_Code')
    st.dataframe(code_name_df)

    # Line Chart of Total Values Over Time
    st.subheader("Total Indicator Values Over Time")
    trend_df = df.groupby('Year')['Value'].sum().reset_index()
    fig_line = px.line(trend_df, x='Year', y='Value', title="Trend of Total Indicator Values Over Time")
    st.plotly_chart(fig_line)

    # Histogram of Value Distribution
    st.subheader("Distribution of Indicator Values")
    fig_hist = px.histogram(df, x='Value', nbins=50, title="Distribution of All Indicator Values")
    st.plotly_chart(fig_hist)

    # Heatmap of Indicator Counts per Year (using Code)
    st.subheader("Indicator Presence Heatmap (by Code and Year)")
    heatmap_data = df.groupby(['Year', 'Indicator_Code']).size().unstack(fill_value=0)
    fig_heat = px.imshow(heatmap_data.T, aspect='auto', title="Indicator Presence Over Years (by Code)")
    st.plotly_chart(fig_heat)

    # Donut Chart of Indicator Counts by Category
    st.subheader("Indicator Count by Category")
    category_counts = {cat: len(indicators) for cat, indicators in categories.items()}
    category_df = pd.DataFrame(list(category_counts.items()), columns=["Category", "Count"])
    fig_donut = px.pie(category_df, names="Category", values="Count", hole=0.5, title="Indicator Distribution by Category")
    st.plotly_chart(fig_donut)


# Trends Over Time
def show_trends_over_time(data, selected_indicators):
    # Filter data based on selected indicators
    chart_data = data[data['Indicator Name'].isin(selected_indicators)]

    # Create the line chart with different colors for each indicator
    fig_line = px.line(chart_data, x="Year", y="Value", color="Indicator Name", title="Trends Over Time")

    # Modify layout to place the legend below the chart and avoid overlap
    fig_line.update_layout(
        legend=dict(
            orientation="h", 
            yanchor="bottom",  
            y=-0.5,  
            xanchor="center",  
            x=0.5, 
            tracegroupgap=0,  
            itemwidth=50,  
            itemsizing='constant',  
        ),
        margin=dict(b=100) 
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig_line)

# Comparative Insights
def show_comparative_insights(df):
    st.title("Comparative Insights")
    
    comparison_indicators = df[df['Indicator Name'].str.contains("comparison", case=False)]
    
    st.write("Indicators for Comparative Insights:")
    st.dataframe(comparison_indicators)

def show_key_indicator_highlights(df):
    st.title("Key Indicator Highlights")
    
    # List of all indicators
    all_indicators = df['Indicator Name'].unique().tolist()
    
    # Let the user select the indicators they want to highlight
    selected_indicators = st.multiselect(
        "Select Key Indicators to Highlight", all_indicators, default=all_indicators[:5]
    )
    
    # Filter data based on selected indicators
    selected_data = df[df['Indicator Name'].isin(selected_indicators)]
    
    # Show the filtered data
    if not selected_data.empty:
        st.write(f"Showing selected key health indicators:")
        st.dataframe(selected_data)
    else:
        st.info("No indicators selected. Please select indicators to display.")


# Demographic Insights
def show_demographic_insights(df):
    st.title("Demographic Insights")
    female_indicators = df[df['Indicator Name'].str.contains("female", case=False)]
    male_indicators = df[df['Indicator Name'].str.contains("male", case=False)]
    children_indicators = df[df['Indicator Name'].str.contains("children", case=False)]

    st.write("Indicators for Female:")
    st.dataframe(female_indicators)
    st.write("Indicators for Male:")
    st.dataframe(male_indicators)
    st.write("Indicators for Children:")
    st.dataframe(children_indicators)

# Expenditure Analysis
def show_expenditure_analysis(df):
    st.title("Expenditure Analysis")
    expenditure_indicators = df[df['Indicator Name'].str.contains("expenditure", case=False)]
    st.write("Indicators related to Health Expenditure:")
    st.dataframe(expenditure_indicators)

# Mortality Trends
def show_mortality_trends(df):
    st.title("Mortality Trends")
    mortality_indicators = df[df['Indicator Name'].str.contains("mortality", case=False)]
    st.write("Indicators related to Mortality:")
    st.dataframe(mortality_indicators)
