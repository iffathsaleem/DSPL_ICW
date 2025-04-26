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

# --------------------------
# Existing Visualizations
# --------------------------

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

# --------------------------
# Advanced Visualizations
# --------------------------

@st.cache_data
def load_geojson():
    """Load Sri Lanka district boundaries"""
    url = "https://raw.githubusercontent.com/rajithaw/geojson-srilanka/master/srilanka.geojson"
    return gpd.read_file(url)

def show_interactive_map(health_data):
    """Display choropleth map of health indicators by district"""
    initialize_page("Sri Lanka Health Map")
    
    try:
        districts = load_geojson()
        
        # Ensure your health_data has 'District' column matching GeoJSON's 'NAME_1'
        if 'District' not in health_data.columns:
            st.warning("District-level data not available in this dataset")
            return
            
        latest_year = health_data['Year'].max()
        indicator = st.selectbox(
            "Select Indicator to Map",
            health_data['Indicator Name'].unique()
        )
        
        filtered = health_data[
            (health_data['Indicator Name'] == indicator) &
            (health_data['Year'] == latest_year)
        ]
        
        merged = districts.merge(
            filtered,
            left_on='NAME_1',
            right_on='District',
            how='left'
        )
        
        m = folium.Map(location=[7.8731, 80.7718], zoom_start=7)
        
        choropleth = folium.Choropleth(
            geo_data=merged,
            name='choropleth',
            data=merged,
            columns=['NAME_1', 'Value'],
            key_on='feature.properties.NAME_1',
            fill_color='YlGn',
            nan_fill_color='gray',
            legend_name=f'{indicator} ({latest_year})'
        ).add_to(m)
        
        # Add tooltips
        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(
                fields=['NAME_1', 'Value'],
                aliases=['District:', 'Value:'],
                style=("font-weight: bold;")
            )
        )
        
        folium_static(m, width=800)
        
    except Exception as e:
        st.error(f"Map rendering failed: {str(e)}")

def show_health_equity(health_data):
    """Analyze health disparities using Gini coefficient"""
    initialize_page("Health Equity Analysis")
    
    def calculate_gini(x):
        x = x.dropna()
        if len(x) == 0:
            return np.nan
        x = np.sort(x)
        n = len(x)
        index = np.arange(1, n+1)
        return ((np.sum((2 * index - n - 1) * x)) / (n * np.sum(x)))
    
    try:
        st.markdown("""
        ### Health Inequality Across Districts
        Measures disparity in health indicators using Gini coefficient
        (0 = perfect equality, 1 = maximum inequality)
        """)
        
        # Calculate Gini for each indicator-year combination
        equity_data = health_data.groupby(['Year', 'Indicator Name'])['Value'].apply(
            calculate_gini
        ).reset_index(name='Gini')
        
        # Top 5 most unequal indicators
        st.subheader("Most Unequal Indicators")
        top_inequality = equity_data.sort_values('Gini', ascending=False).head(5)
        st.dataframe(top_inequality)
        
        # Time trend visualization
        indicator = st.selectbox(
            "Select Indicator to View Trend",
            equity_data['Indicator Name'].unique()
        )
        
        fig = px.line(
            equity_data[equity_data['Indicator Name'] == indicator],
            x='Year',
            y='Gini',
            title=f'Inequality Trend for {indicator}',
            markers=True
        )
        fig.update_yaxes(range=[0, 1])
        st.plotly_chart(fig)
        
    except Exception as e:
        st.error(f"Equity analysis failed: {str(e)}")

def show_forecasting(health_data):
    """ARIMA forecasting of health indicators"""
    initialize_page("Health Indicator Forecasting")
    
    indicator = st.selectbox(
        "Select Indicator to Forecast", 
        health_data['Indicator Name'].unique(),
        key='forecast_indicator'
    )
    
    try:
        ts_data = health_data[health_data['Indicator Name'] == indicator]
        ts_data = ts_data.set_index('Year')['Value'].sort_index()
        
        if len(ts_data) < 5:
            st.warning("Minimum 5 years of data required for forecasting")
            return
            
        col1, col2 = st.columns(2)
        with col1:
            steps = st.slider("Forecast Period (years)", 1, 10, 5)
        with col2:
            train_years = st.slider(
                "Training Data Years", 
                min_value=int(ts_data.index.min()),
                max_value=int(ts_data.index.max()),
                value=(int(ts_data.index.min()), int(ts_data.index.max()))
            )
        
        train_data = ts_data[(ts_data.index >= train_years[0]) & 
                            (ts_data.index <= train_years[1])]
        
        model = ARIMA(train_data, order=(1,1,1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=steps)
        
        # Create visualization
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=train_data.index,
            y=train_data,
            name='Historical Data',
            line=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=forecast.index,
            y=forecast,
            name='Forecast',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(
            title=f'{steps}-Year Forecast for {indicator}',
            xaxis_title='Year',
            yaxis_title='Value'
        )
        
        st.plotly_chart(fig)
        
        # Show forecast values
        with st.expander("View Forecast Values"):
            st.dataframe(forecast.to_frame(name='Predicted Value'))
            
    except Exception as e:
        st.error(f"Forecasting failed: {str(e)}")

def show_data_explorer(health_data):
    """Interactive data query and visualization tool"""
    initialize_page("Data Explorer")
    
    st.subheader("Query and Visualize Data")
    
    # Query builder
    col1, col2 = st.columns(2)
    with col1:
        year_range = st.slider(
            "Year Range",
            min_value=int(health_data['Year'].min()),
            max_value=int(health_data['Year'].max()),
            value=(int(health_data['Year'].min()), int(health_data['Year'].max())))
    with col2:
        keyword = st.text_input("Filter by keyword (e.g. 'mortality')", "")
    
    # Apply filters
    filtered = health_data[
        (health_data['Year'].between(year_range[0], year_range[1])) &
        (health_data['Indicator Name'].str.contains(keyword, case=False) if keyword else True)
    ]
    
    if filtered.empty:
        st.warning("No data matches your filters")
        return
    
    # Visualization options
    st.subheader("Create Custom Visualization")
    
    chart_type = st.selectbox(
        "Chart Type",
        ["Line Chart", "Bar Chart", "Scatter Plot", "Box Plot"]
    )
    
    cols = st.columns(2)
    with cols[0]:
        x_axis = st.selectbox(
            "X-Axis",
            filtered.columns,
            index=list(filtered.columns).index('Year')
        )
    with cols[1]:
        y_axis = st.selectbox(
            "Y-Axis",
            filtered.columns,
            index=list(filtered.columns).index('Value')
        )
    
    # Generate chart
    if chart_type == "Line Chart":
        fig = px.line(
            filtered,
            x=x_axis,
            y=y_axis,
            color='Indicator Name',
            title=f"{y_axis} by {x_axis}"
        )
    elif chart_type == "Bar Chart":
        fig = px.bar(
            filtered,
            x=x_axis,
            y=y_axis,
            color='Indicator Name',
            barmode='group'
        )
    elif chart_type == "Scatter Plot":
        fig = px.scatter(
            filtered,
            x=x_axis,
            y=y_axis,
            color='Indicator Name',
            hover_name='Indicator Name'
        )
    else:  # Box Plot
        fig = px.box(
            filtered,
            x=x_axis,
            y=y_axis,
            color='Indicator Name'
        )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show raw data
    with st.expander("View Filtered Data"):
        st.dataframe(filtered.sort_values(['Year', 'Indicator Name']))