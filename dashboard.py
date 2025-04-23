import streamlit as st
import pandas as pd
import plotly.express as px
from sidebar import sidebar_filters
from categories import categories, map_category
from visualizations import show_bullet_graph

health = pd.read_csv("Sri Lanka Health Statistics.csv")

health['Category'] = health['Indicator Name'].apply(map_category)

# Background image mapping for categories
background_images = {
    "About": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/About.jpg",
    "Overview Dashboard": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Overview.jpg",  
    "Trends Over Time": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Trends%20Overtime.JPG", 
    "Demographic Insights": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Demographic%20Insights.jpg",
    "Expenditure Analysis": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Expenditure%20Analysis.jpg",  
    "Mortality & Morbidity": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Mortality%20%26%20Morbidity.jpg",  
    "Comparative Insights": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Comparative%20Insights.jpg",  
    "Key Indicator Highlights": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Key%20Indicator%20Highlights.jpg",  
    "Maternal and Child Health": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Maternal%20and%20Child%20Health.jpg",  
    "Infectious Diseases": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Infectious%20Diseases.jpg",  
    "Nutrition and Food Security": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Nutrition%20and%20Food%20Security.jpg",  
    "Health Expenditures": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Health%20Expenditures.jpg",  
    "Population Health and Demographics": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Population%20Health%20and%20Demographics.jpg", 
    "Mortality Rates": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Mortality%20Rates.jpeg"  
}

# Sidebar image URL
sidebar_image_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Sidebar.png"

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
def show_dashboard(health, category, selected_indicators, year_range, sort_order, keyword_filter):
    set_sidebar_background(sidebar_image_url)

    image_url = background_images.get(category, None)
    if image_url:
        set_background(image_url)

    st.title("Health Data Dashboard")
    start_year, end_year = year_range

    # Filter by year
    filtered = health[health['Year'].between(start_year, end_year)]

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
def show_overview_dashboard(health):
    set_background(background_images["Overview Dashboard"])
    st.title("Overview Dashboard")

    # Basic Stats
    total_indicators = health['Indicator Name'].nunique()
    total_records = len(health)
    years_covered = health['Year'].nunique()
    earliest_year = health['Year'].min()
    latest_year = health['Year'].max()
    avg_value = health['Value'].mean()

    most_frequent_indicator = health['Indicator Name'].value_counts().idxmax()
    top_avg_indicator = health.groupby('Indicator Name')['Value'].mean().idxmax()
    max_value_row = health.loc[health['Value'].idxmax()]
    min_value_row = health.loc[health['Value'].idxmin()]

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
    st.dataframe(health)

    # Indicator Groups

# Indicator Groups
st.subheader("Indicator Groupings")
for group in categories:
    st.markdown(f"**{group}**")
    st.markdown("• " + "<br>• ".join(categories[group]), unsafe_allow_html=True)

# Bar Chart of Indicator Frequency (using Indicator Code)
st.subheader("Indicator Frequency by Code")
freq_health = health['Indicator_Code'].value_counts().reset_index()
freq_health.columns = ['Indicator_Code', 'Count']
fig_bar = px.bar(freq_health, x='Indicator_Code', y='Count', title="Frequency of Each Indicator (Code)")
st.plotly_chart(fig_bar)

# Code-to-Name Legend Table
st.markdown("**Indicator Code Reference Table**")
code_name_health = health[['Indicator_Code', 'Indicator Name']].drop_duplicates().sort_values('Indicator_Code')
st.dataframe(code_name_health)

# Line Chart of Total Values Over Time
st.subheader("Total Indicator Values Over Time")
trend_health = health.groupby('Year')['Value'].sum().reset_index()
fig_line = px.line(trend_health, x='Year', y='Value', title="Trend of Total Indicator Values Over Time")
st.plotly_chart(fig_line)

# Histogram of Value Distribution
st.subheader("Distribution of Indicator Values")
fig_hist = px.histogram(health, x='Value', nbins=50, title="Distribution of All Indicator Values")
st.plotly_chart(fig_hist)

# Heatmap of Indicator Counts per Year (using Code)
st.subheader("Indicator Presence Heatmap (by Code and Year)")
heatmap_data = health.groupby(['Year', 'Indicator_Code']).size().unstack(fill_value=0)
fig_heat = px.imshow(heatmap_data.T, aspect='auto', title="Indicator Presence Over Years (by Code)")
st.plotly_chart(fig_heat)

# Donut Chart of Indicator Counts by Category using map_category
st.subheader("Indicator Count by Category")
category_counts = {}
for indicator in health['Indicator Name'].unique():
    category = map_category(indicator)
    if category not in category_counts:
        category_counts[category] = 0
    category_counts[category] += 1

category_health = pd.DataFrame(list(category_counts.items()), columns=["Category", "Count"])
fig_donut = px.pie(category_health, names="Category", values="Count", hole=0.5, title="Indicator Distribution by Category")
st.plotly_chart(fig_donut)

# Trends Over Time
def show_trends_over_time(data):
    set_background(background_images["Trends Over Time"])
    st.title("Trends Over Time by Category")

    for category_name, indicators in categories.items():
        # Filter data for indicators in this category
        category_data = data[data['Indicator Name'].isin(indicators)]

        if category_data.empty:
            continue  

        # Create a line chart for this category
        fig_line = px.line(
            category_data,
            x="Year",
            y="Value",
            color="Indicator Name",
            title=f"{category_name} Trends Over Time"
        )

        fig_line.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.7,
                xanchor="center",
                x=0.5,
                tracegroupgap=0,
                itemwidth=50,
                itemsizing='constant',
            ),
            margin=dict(b=100)
        )

        st.plotly_chart(fig_line)


# Comparative Insights
def show_comparative_insights(health):
    set_background(background_images["Comparative Insights"])
    st.title("Comparative Insights")
    
    # Line Chart for Life Expectancy at Birth (Female and Male)
    life_expectancy_indicators = [
        "Life expectancy at birth, female (years)", 
        "Life expectancy at birth, male (years)"
    ]
    
    life_expectancy_data = health[health['Indicator Name'].isin(life_expectancy_indicators)]

    if life_expectancy_data.empty:
        st.warning("No data available for life expectancy indicators.")
    else:
        st.subheader("Life Expectancy at Birth (Female & Male)")
        
        fig_life_expectancy = px.line(
            life_expectancy_data,
            x='Year',
            y='Value',
            color='Indicator Name',
            markers=True,  # Add markers to data points
            color_discrete_map={
                "Life expectancy at birth, female (years)": "blue",
                "Life expectancy at birth, male (years)": "green"
            },
            title="Life Expectancy at Birth: Female vs Male"
        )
        
        fig_life_expectancy.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.6,
                xanchor="center",
                x=0.5
            ),
            margin=dict(b=100),
            xaxis=dict(
                title="Year"
            )
        )
        st.plotly_chart(fig_life_expectancy)
    

def show_key_indicator_highlights(health):
    set_background(background_images["Key Indicator Highlights"])
    st.title("Key Indicator Highlights")

    all_indicators = health['Indicator Name'].unique().tolist()

    selected_indicators = st.multiselect(
        "Select Key Indicators to Highlight",
        options=all_indicators,
        default=all_indicators[:5]
    )

    if not selected_indicators:
        st.info("Please select at least one indicator to view highlights and bullet graphs.")
        return

    year_range = st.slider(
    "Select Year Range",
    min_value=int(health['Year'].min()),
    max_value=int(health['Year'].max()),
    value=(int(health['Year'].min()), int(health['Year'].max())),
    step=1,
    key="year_slider"  # Make sure this key is unique
)

    selected_data = health[
        (health['Indicator Name'].isin(selected_indicators)) &
        (health['Year'].between(year_range[0], year_range[1]))
    ]

    st.write("Displaying data and bullet graphs for selected key health indicators:")
    st.dataframe(selected_data)

    target_value = 75

    for indicator in selected_indicators:
        show_bullet_graph(health, indicator, target_value, year_range)

# Demographic Insights
def show_demographic_insights(health):
    set_background(background_images["Demographic Insights"])
    st.title("Demographic Insights")
    female_indicators = health[health['Indicator Name'].str.contains("female", case=False)]
    male_indicators = health[health['Indicator Name'].str.contains("male", case=False)]
    children_indicators = health[health['Indicator Name'].str.contains("children", case=False)]

    st.write("Indicators for Female:")
    st.dataframe(female_indicators)
    st.write("Indicators for Male:")
    st.dataframe(male_indicators)
    st.write("Indicators for Children:")
    st.dataframe(children_indicators)

# Expenditure Analysis
def show_expenditure_analysis(health):
    set_background(background_images["Expenditure Analysis"])
    st.title("Expenditure Analysis")
    expenditure_indicators = health[health['Indicator Name'].str.contains("expenditure", case=False)]
    st.write("Indicators related to Health Expenditure:")
    st.dataframe(expenditure_indicators)

# Mortality Trends
def show_mortality_trends(health):
    set_background(background_images["Mortality & Morbidity"])
    st.title("Mortality Trends")
    
    # Get mortality indicators from categories.py
    mortality_indicators = categories.get("Mortality Rates", [])

    st.markdown("**Indicators related to Mortality:**")
    st.markdown("• " + "<br>• ".join(mortality_indicators), unsafe_allow_html=True)

    # Filter data
    mortality_data = health[health['Indicator Name'].isin(mortality_indicators)]

    if mortality_data.empty:
        st.warning("No data available for mortality indicators.")
        return

    # Show data
    st.dataframe(mortality_data)

def show_pie_chart(data, category_name, relevant_indicators=None):
    st.subheader(f"{category_name} Breakdown")
    
    # Filter the data based on category
    category_data = data[data['Category'] == category_name]
    
    # Filter the data for the relevant indicators, if provided
    if relevant_indicators:
        category_data = category_data[category_data['Indicator Name'].isin(relevant_indicators)]
    
    # Get the years from 1960 to 2023 (or the available range)
    years = sorted(category_data['Year'].unique())
    
    # Iterate over each year and create a pie chart
    for year in years:
        year_data = category_data[category_data['Year'] == year]
        
        if year_data.empty:
            st.warning(f"No data available for {category_name} in {year}.")
            continue
        
        # Summarize data by the Indicator Name
        summary = year_data.groupby('Indicator Name')['Value'].mean().reset_index()
        
        # Create pie chart for this year
        fig = px.pie(summary, names='Indicator Name', values='Value', 
                     title=f"Indicator Contribution in {category_name} ({year})", hole=0.3)
        st.plotly_chart(fig)

# Usage for Maternal and Child Health
def show_maternal_child_piecharts(data):
    set_background(background_images["Maternal and Child Health"])
    show_pie_chart(data, 'Maternal and Child Health')

# Usage for Infectious Diseases
def show_infectious_diseases_piecharts(data):
    set_background(background_images["Infectious Diseases"])
    show_pie_chart(data, 'Infectious Diseases')

# Usage for Nutrition and Food Security
def show_nutrition_foodsecurity_piecharts(data):
    set_background(background_images["Nutrition and Food Security"])
    show_pie_chart(data, 'Nutrition and Food Security')

# Usage for Health Expenditures
def show_expenditure_piecharts(data):
    set_background(background_images["Health Expenditures"])
    show_pie_chart(data, 'Health Expenditures')

def show_population_piecharts(data):
    set_background(background_images["Population Health and Demographics"])
    relevant_indicators = [
        "Life expectancy at birth, female (years)",
        "Life expectancy at birth, male (years)",
        "Population growth (annual %)",
        "Population, female",
        "Population, male",
        "Women who were first married by age 18 (% of women ages 20-24)"
    ]
    
    # Filter the data for Population Health and Demographics
    category_data = data[data['Category'] == 'Population Health and Demographics']
    
    # Filter the data for the relevant indicators
    relevant_data = category_data[category_data['Indicator Name'].isin(relevant_indicators)]
    
    # Get the years from 1960 to 2023 (or the available range)
    years = sorted(relevant_data['Year'].unique())
    
    # Iterate over each year and create a pie chart
    for year in years:
        year_data = relevant_data[relevant_data['Year'] == year]
        
        # Summarize the relevant data by averaging the 'Value' for each indicator
        summary = year_data.groupby('Indicator Name')['Value'].mean().reset_index()

        # Ensure there are no zero or NaN values for the pie chart
        summary = summary[summary['Value'] > 0]
        
        # Create pie chart with proper values
        fig = px.pie(summary, names='Indicator Name', values='Value', 
                     title=f"Indicator Contribution in Population Health and Demographics ({year})", hole=0.3)
        st.plotly_chart(fig)

# Usage for Mortality Rates
def show_mortality_piecharts(data):
    set_background(background_images["Mortality Rates"])
    show_pie_chart(data, 'Mortality Rates')
