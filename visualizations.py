import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Radar Chart
def show_radar_chart(health, category):
    st.subheader(f"Radar Chart: Indicator Comparison for {category}")
    category_data = health[health['Category'] == category]
    indicators = category_data['Indicator Name'].unique()

    if len(indicators) == 0:
        st.info("No indicators available in this category to display a radar chart.")
        return

    values = [category_data[category_data['Indicator Name'] == indicator]['Value'].mean() for indicator in indicators]
    radar_data = pd.DataFrame({'Indicator': indicators, 'Value': values})
    fig = px.line_polar(radar_data, r='Value', theta='Indicator', line_close=True)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)

# Animated Line Chart
def show_animated_line_chart(health):
    st.subheader("Animated Line Chart: Trends Over Time")
    fig = px.line(
        health, x='Year', y='Value', color='Indicator Name', animation_frame='Year',
        title="Trends Over Time - Animated View"
    )
    st.plotly_chart(fig)

# Stacked Area Chart
def show_stacked_area_chart(health):
    st.subheader("Stacked Area Chart: Category Contributions Over Time")
    fig = px.area(
        health, x='Year', y='Value', color='Category', line_group='Category',
        title="Stacked Area Chart of Categories"
    )
    st.plotly_chart(fig)

# Bullet Graph
def show_bullet_graph(health, indicator, target_value, year_range):
    st.subheader("Key Indicator - Bullet Graph")

    if not indicator:
        st.info("Please select an indicator from the sidebar to display the bullet graph.")
        return

    # Ensure the 'Value' column is numeric
    health['Value'] = pd.to_numeric(health['Value'], errors='coerce')

    # Filter the data for the selected indicator and year range
    indicator_data = health[
        (health['Indicator Name'] == indicator) & 
        (health['Year'].between(year_range[0], year_range[1]))
    ].dropna(subset=['Value', 'Year'])

    if indicator_data.empty:
        st.warning("No data available for the selected indicator and year range.")
        return

    # Group the data by year and calculate the mean value for each year
    indicator_data = indicator_data.groupby('Year', as_index=False)['Value'].mean()

    for _, row in indicator_data.iterrows():
        actual = row['Value']
        year = row['Year']

        # Create the figure for each year
        fig = go.Figure()

        # Target Bar
        fig.add_trace(go.Bar(
            x=[target_value],
            y=[str(year)],
            orientation='h',
            marker=dict(color='lightgray'),
            name='Target',
            hoverinfo='skip'
        ))

        # Actual Bar
        fig.add_trace(go.Bar(
            x=[actual],
            y=[str(year)],
            orientation='h',
            marker=dict(color='steelblue'),
            name='Actual'
        ))

        # Target Marker
        fig.add_trace(go.Scatter(
            x=[target_value],
            y=[str(year)],
            mode='markers',
            marker=dict(symbol='line-ns-open', color='red', size=12),
            name='Target Marker'
        ))

        # Layout settings for the graph
        fig.update_layout(
            barmode='overlay',
            title=f"{indicator} ({int(year)})",
            xaxis=dict(title='Value'),
            yaxis=dict(title='Year'),
            height=200
        )

        st.plotly_chart(fig)