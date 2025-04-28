import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from statsmodels.tsa.arima.model import ARIMA
from dashboard import initialize_page

def show_comparative_chart(data, indicators, title, color_map=None):
    """Display a comparative line chart for multiple indicators"""
    filtered_data = data[data['Indicator Name'].isin(indicators)]
    
    if filtered_data.empty:
        st.warning(f"No data available for the selected indicators.")
        return
    
    fig = px.line(
        filtered_data,
        x='Year',
        y='Value',
        color='Indicator Name',
        markers=True,
        color_discrete_map=color_map,
        title=title,
        labels={'Value': 'Value', 'Year': 'Year'}
    )
    
    fig.update_layout(
        height=500,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.6,
            xanchor="center",
            x=0.5
        ),
        margin=dict(b=100),
        xaxis=dict(title="Year")
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_pie_chart(data, category_name, relevant_indicators=None):
    """Display pie charts for category breakdown"""
    st.subheader(f"{category_name} Breakdown")
    
    category_data = data[data['Category'] == category_name]
    
    if relevant_indicators:
        category_data = category_data[category_data['Indicator Name'].isin(relevant_indicators)]
    
    years = sorted(category_data['Year'].unique())
    
    for year in years:
        year_data = category_data[category_data['Year'] == year]
        
        if year_data.empty:
            st.warning(f"No data available for {category_name} in {year}.")
            continue
        
        summary = year_data.groupby('Indicator Name')['Value'].mean().reset_index()
        
        fig = px.pie(
            summary, 
            names='Indicator Name', 
            values='Value', 
            title=f"Indicator Contribution in {category_name} ({year})", 
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)

def show_stacked_area_chart(health_data):
    st.subheader("Population Composition Over Time")
    try:
        fig = px.area(
            health_data,
            x='Year', 
            y='Value',
            color='Indicator Name',
            line_group='Indicator Name',
            title="Population Demographic Trends"
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error generating area chart: {str(e)}")

def show_population_piecharts(data):
    st.subheader("Population Breakdowns")
    years = sorted(data['Year'].unique())
    
    for year in years[-3:]:  # Show last 3 years
        year_data = data[data['Year'] == year]
        if not year_data.empty:
            fig = px.pie(
                year_data,
                names='Indicator Name',
                values='Value',
                title=f"Population Distribution ({year})",
                hole=0.3
            )
            st.plotly_chart(fig, use_container_width=True)

# Fix the show_comparative_chart function (remove duplicate)
def show_comparative_chart(data, indicators, title, color_map=None):
    """Display a comparative line chart for multiple indicators"""
    filtered_data = data[data['Indicator Name'].isin(indicators)]
    
    if filtered_data.empty:
        st.warning(f"No data available for the selected indicators.")
        return

    fig = px.line(
        filtered_data,
        x='Year',
        y='Value',
        color='Indicator Name',
        markers=True,
        color_discrete_map=color_map,
        title=title,
        labels={'Value': 'Value', 'Year': 'Year'}
    )
    
    fig.update_layout(
        height=500,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.6,
            xanchor="center",
            x=0.5
        ),
        margin=dict(b=100),
        xaxis=dict(title="Year")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
def show_pie_chart(data, category_name, relevant_indicators=None):
    """Display pie charts for category breakdown"""
    st.subheader(f"{category_name} Breakdown")
    
    category_data = data[data['Category'] == category_name]
    
    if relevant_indicators:
        category_data = category_data[category_data['Indicator Name'].isin(relevant_indicators)]
    
    years = sorted(category_data['Year'].unique())
    
    for year in years:
        year_data = category_data[category_data['Year'] == year]
        
        if year_data.empty:
            st.warning(f"No data available for {category_name} in {year}.")
            continue
        
        summary = year_data.groupby('Indicator Name')['Value'].mean().reset_index()
        
        fig = px.pie(
            summary, 
            names='Indicator Name', 
            values='Value', 
            title=f"Indicator Contribution in {category_name} ({year})", 
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)


def load_geojson():
    """Load Sri Lanka district boundaries"""
    url = "https://raw.githubusercontent.com/rajithaw/geojson-srilanka/master/srilanka.geojson"
    return gpd.read_file(url)

def show_interactive_map(health_data):
    """Simplified Sri Lanka map visualization"""
    initialize_page("Sri Lanka Overview")
    
    # Create base map centered on Sri Lanka
    m = folium.Map(location=[7.8731, 80.7718], zoom_start=7)
    
    # Add country outline (simplified coordinates)
    folium.PolyLine(
        locations=[
            [9.8, 79.9], [9.1, 80.4], [8.3, 81.0], [7.5, 81.7], 
            [6.0, 81.5], [5.9, 80.5], [6.8, 79.9], [9.8, 79.9]
        ],
        color='blue',
        weight=2
    ).add_to(m)
    
    # Add marker for capital
    folium.Marker(
        [6.9271, 79.8612],
        popup="Colombo",
        icon=folium.Icon(color='red')
    ).add_to(m)
    
    folium_static(m, width=800)

def render_visualization(data, sort_order):
    """Helper function to render the selected visualization"""
    st.markdown("## Data Visualization")
    
    # Chart type selection
    chart_type = st.selectbox(
        "Chart Type",
        ["Line Chart", "Bar Chart", "Scatter Plot", "Box Plot"],
        key="viz_chart_type"
    )
    
    # Generate the appropriate chart
    if chart_type == "Line Chart":
        fig = px.line(
            data, 
            x='Year', 
            y='Value', 
            color='Indicator Name',
            title="Trend Over Time"
        )
    elif chart_type == "Bar Chart":
        fig = px.bar(
            data,
            x='Year',
            y='Value',
            color='Indicator Name',
            barmode='group',
            title="Comparison by Year"
        )
    elif chart_type == "Scatter Plot":
        fig = px.scatter(
            data,
            x='Year',
            y='Value',
            color='Indicator Name',
            hover_name='Indicator Name',
            title="Value Distribution"
        )
    else:  # Box Plot
        fig = px.box(
            data,
            x='Indicator Name',
            y='Value',
            color='Indicator Name',
            title="Statistical Distribution"
        )
    
    # Standardize layout with legend below
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.3,  # Positions legend below chart
            xanchor="center",
            x=0.5
        ),
        margin=dict(b=100)  # Adds bottom margin
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show filtered data table
    with st.expander("View Filtered Data"):
        st.dataframe(
            data.sort_values(
                ['Year', 'Value'],
                ascending=(sort_order == "Ascending")
            ),
            height=300
        )

def show_data_explorer(health_data):
    """Interactive data explorer with visualization options"""
    initialize_page("Data Explorer")
    
    st.markdown("""
    ## Data Explorer
    Adjust filters in the sidebar to update the visualization below.
    """)
    
    # Get filters from session state
    if 'current_filters' not in st.session_state:
        st.warning("Please configure filters in the sidebar first.")
        return
    
    filters = st.session_state.current_filters
    
    # Apply all filters
    filtered = health_data[
        (health_data['Year'].between(filters['year_range'][0], filters['year_range'][1])) &
        (health_data['Indicator Name'].isin(filters['indicators']))
    ]
    
    if filters.get('keyword') and filters['keyword'] != "All":
        filtered = filtered[filtered['Indicator Name'].str.contains(
            filters['keyword'], case=False)]
    
    if filters.get('category') and filters['category'] != "All":
        filtered = filtered[filtered['Category'] == filters['category']]
    
    # Show visualization or empty state message
    if filtered.empty:
        st.warning("No data matches current filters. Try broadening your criteria.")
    else:
        render_visualization(filtered, filters.get('sort_order', "Ascending"))