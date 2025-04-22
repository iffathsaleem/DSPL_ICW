import streamlit as st
import pandas as pd
import plotly.express as px
from sidebar import sidebar_filters

df = pd.read_csv("Sri Lanka Health Statistics.csv")

# Get the sidebar filter values
category, selected_indicators, year_range, sort_order, keyword_filter = sidebar_filters(df)

# Filter data based on selected indicators and year range
filtered_df = df[df['Indicator Name'].isin(selected_indicators)]
filtered_df = filtered_df[(filtered_df['Year'] >= year_range[0]) & (filtered_df['Year'] <= year_range[1])]

# Now, use the 'category' value directly for the background or other category-specific logic
background_url = get_selected_category_image(category)  # You might need to adjust this based on your category logic
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

st.subheader("Key Metrics Overview")
latest_year = filtered_df['Year'].max()
latest_data = filtered_df[filtered_df['Year'] == latest_year]
top_indicators = latest_data.nlargest(5, 'Value')
for _, row in top_indicators.iterrows():
    st.metric(label=row['Indicator Name'], value=f"{row['Value']:.2f}", delta=f"Year: {int(row['Year'])}")

st.subheader("Trends Over Time")
trend_indicators = filtered_df['Indicator Name'].unique()
selected_trend = st.selectbox("Select Indicator for Trend", trend_indicators)
trend_df = filtered_df[filtered_df['Indicator Name'] == selected_trend]
fig_trend = px.line(trend_df, x='Year', y='Value', color='Indicator Name', markers=True)
st.plotly_chart(fig_trend, use_container_width=True)

st.subheader("Contribution Breakdown")
latest = filtered_df[filtered_df['Year'] == latest_year]
fig_pie = px.pie(latest, names='Indicator Name', values='Value', title=f"Indicator Breakdown in {int(latest_year)}")
st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("Demographic Breakdown")
demo_df = filtered_df[filtered_df['Indicator Name'].str.contains('female|male|age|children|kids|adolescent', case=False)]
if not demo_df.empty:
    fig_demo = px.bar(demo_df, x='Indicator Name', y='Value', color='Year', barmode='group', title="Demographic Indicator Comparison")
    st.plotly_chart(fig_demo, use_container_width=True)

st.subheader("Radar Chart: Indicator Comparison")
radar_df = latest_data.copy()
fig_radar = px.line_polar(radar_df, r='Value', theta='Indicator Name', line_close=True, title="Radar Chart of Indicators")
st.plotly_chart(fig_radar, use_container_width=True)

st.subheader("Indicator Relationships (Scatter Plot)")
if len(filtered_df['Indicator Name'].unique()) >= 2:
    options = list(filtered_df['Indicator Name'].unique())
    x_ind = st.selectbox("Select X-Axis Indicator", options)
    y_ind = st.selectbox("Select Y-Axis Indicator", options, index=1)
    
    x_df = filtered_df[filtered_df['Indicator Name'] == x_ind][['Year', 'Value']].rename(columns={'Value': x_ind})
    y_df = filtered_df[filtered_df['Indicator Name'] == y_ind][['Year', 'Value']].rename(columns={'Value': y_ind})
    merged_df = pd.merge(x_df, y_df, on='Year')
    fig_scatter = px.scatter(merged_df, x=x_ind, y=y_ind, trendline="ols", title=f"{y_ind} vs {x_ind}")
    st.plotly_chart(fig_scatter, use_container_width=True)

if category.lower() == "mortality rates":
    st.subheader("Mortality Trends Over Time")
    mortality_df = filtered_df.copy()
    fig_mortality = px.line(mortality_df, x='Year', y='Value', color='Indicator Name', markers=True)
    st.plotly_chart(fig_mortality, use_container_width=True)

if category.lower() == "health expenditures":
    st.subheader("Health Expenditure Insights")
    exp_df = filtered_df.copy()
    fig_exp = px.bar(exp_df, x='Year', y='Value', color='Indicator Name', barmode='stack')
    st.plotly_chart(fig_exp, use_container_width=True)
