import streamlit as st
import pandas as pd
import plotly.express as px
from sidebar import filter_data_by_keywords, get_selected_category_image

# Load data
df = pd.read_csv("Sri Lanka Health Statistics.csv")
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

# Sidebar filters
st.sidebar.header("Filter Indicators")
keyword_filter = st.sidebar.text_input("Keyword (e.g., 'female', 'kids', 'all')").lower()
year_range = st.sidebar.slider("Select Year Range", int(df['Year'].min()), int(df['Year'].max()), (int(df['Year'].min()), int(df['Year'].max())))

# Filter by keyword and year
filtered_df = filter_data_by_keywords(df, keyword_filter)
filtered_df = filtered_df[(filtered_df['Year'] >= year_range[0]) & (filtered_df['Year'] <= year_range[1])]

# Category selection
category = st.selectbox("Select a Health Category", df['Category'].unique())
category_df = filtered_df[filtered_df['Category'] == category]

# Set background image
background_url = get_selected_category_image(category)
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url("{background_url}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
""", unsafe_allow_html=True)

st.title(f"{category} Dashboard")

# 1. Key Metrics Overview
st.subheader("Key Metrics Overview")
latest_year = category_df['Year'].max()
latest_data = category_df[category_df['Year'] == latest_year]
top_indicators = latest_data.nlargest(5, 'Value')
for _, row in top_indicators.iterrows():
    st.metric(label=row['Indicator'], value=f"{row['Value']:.2f}", delta=f"Year: {int(row['Year'])}")

# 2. Trend Analysis
st.subheader("Trends Over Time")
trend_indicators = category_df['Indicator'].unique()
selected_trend = st.selectbox("Select Indicator for Trend", trend_indicators)
trend_df = category_df[category_df['Indicator'] == selected_trend]
fig_trend = px.line(trend_df, x='Year', y='Value', color='Indicator', markers=True)
st.plotly_chart(fig_trend, use_container_width=True)

# 3. Pie Chart by Indicator Contribution
st.subheader("Contribution Breakdown")
latest = category_df[category_df['Year'] == latest_year]
fig_pie = px.pie(latest, names='Indicator', values='Value', title=f"{category} Breakdown in {int(latest_year)}")
st.plotly_chart(fig_pie, use_container_width=True)

# 4. Bar Chart by Gender/Age Group
st.subheader("Demographic Breakdown")
demo_df = category_df[category_df['Indicator'].str.contains('female|male|age|children|kids|adolescent', case=False)]
if not demo_df.empty:
    fig_demo = px.bar(demo_df, x='Indicator', y='Value', color='Year', barmode='group', title="Demographic Indicator Comparison")
    st.plotly_chart(fig_demo, use_container_width=True)

# 5. Radar Chart 
st.subheader("Radar Chart: Indicator Comparison")
radar_df = latest_data.copy()
fig_radar = px.line_polar(radar_df, r='Value', theta='Indicator', line_close=True, title="Radar Chart of Indicators")
st.plotly_chart(fig_radar, use_container_width=True)

# 6. Scatter Plot 
st.subheader("Indicator Relationships (Scatter Plot)")
if len(category_df['Indicator'].unique()) >= 2:
    options = list(category_df['Indicator'].unique())
    x_ind = st.selectbox("Select X-Axis Indicator", options)
    y_ind = st.selectbox("Select Y-Axis Indicator", options, index=1)
    
    x_df = category_df[category_df['Indicator'] == x_ind][['Year', 'Value']].rename(columns={'Value': x_ind})
    y_df = category_df[category_df['Indicator'] == y_ind][['Year', 'Value']].rename(columns={'Value': y_ind})
    merged_df = pd.merge(x_df, y_df, on='Year')
    fig_scatter = px.scatter(merged_df, x=x_ind, y=y_ind, trendline="ols", title=f"{y_ind} vs {x_ind}")
    st.plotly_chart(fig_scatter, use_container_width=True)

# 7. Mortality Trends 
if category.lower() == "mortality rates":
    st.subheader("Mortality Trends Over Time")
    mortality_df = category_df.copy()
    fig_mortality = px.line(mortality_df, x='Year', y='Value', color='Indicator', markers=True)
    st.plotly_chart(fig_mortality, use_container_width=True)

# 8. Expenditure Analysis
if category.lower() == "health expenditures":
    st.subheader("Health Expenditure Insights")
    exp_df = category_df.copy()
    fig_exp = px.bar(exp_df, x='Year', y='Value', color='Indicator', barmode='stack')
    st.plotly_chart(fig_exp, use_container_width=True)
