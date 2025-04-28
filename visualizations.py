import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
from statsmodels.tsa.arima.model import ARIMA
from dashboard import initialize_page

# Initialize CSS styles (only once)
def initialize_visualization():
    st.markdown("""
    <style>
    .viz-container {
        background-color: rgba(255, 255, 255, 0.88) !important;
        padding: 20px !important;
        border-radius: 10px !important;
        margin: 15px 0 !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    .viz-title {
        color: #000000 !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        margin-bottom: 15px !important;
    }
    .plotly-container {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Comparative line chart
def show_comparative_chart(data, indicators, title, color_map=None):
    initialize_visualization()
    filtered_data = data[data['Indicator Name'].isin(indicators)]
    
    if filtered_data.empty:
        st.warning("No data available for the selected indicators.")
        return

    st.markdown('<div class="viz-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="viz-title">{title}</div>', unsafe_allow_html=True)
    st.markdown('<div class="plotly-container">', unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Pie charts for category breakdown
def show_pie_chart(data, category_name, relevant_indicators=None):
    initialize_visualization()
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

# Stacked area chart for population
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

# Pie charts for population breakdowns
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

# Interactive map
def show_interactive_map(health_data=None):
    initialize_page("Sri Lanka Overview")
    
    st.markdown("### Geographic Context")
    st.markdown("Sri Lanka is an island country in South Asia with diverse geographic features.")

    m = folium.Map(location=[7.8731, 80.7718], zoom_start=7)

    folium.PolyLine(
        locations=[
            [9.8, 79.9], [9.1, 80.4], [8.3, 81.0], [7.5, 81.7],
            [6.0, 81.5], [5.9, 80.5], [6.8, 79.9], [9.8, 79.9]
        ],
        color='blue',
        weight=2,
        fill=True,
        fill_color='blue',
        fill_opacity=0.1
    ).add_to(m)

    cities = [
        {"name": "Colombo", "coords": [6.9271, 79.8612], "pop": "Commercial Capital"},
        {"name": "Kandy", "coords": [7.2906, 80.6337], "pop": "Cultural Capital"},
        {"name": "Galle", "coords": [6.0535, 80.2210], "pop": "Historic Fort City"},
        {"name": "Jaffna", "coords": [9.6615, 80.0255], "pop": "Northern Capital"},
        {"name": "Trincomalee", "coords": [8.5922, 81.2357], "pop": "Natural Harbor"}
    ]

    for city in cities:
        folium.Marker(
            location=city["coords"],
            popup=f"<b>{city['name']}</b><br>{city['pop']}",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

    folium.Marker(
        [6.9934, 81.0550],
        popup="<b>Adam's Peak</b><br>Sacred mountain",
        icon=folium.Icon(color='green', icon='tree-deciduous')
    ).add_to(m)

    folium.Marker(
        [6.0333, 80.2167],
        popup="<b>Unawatuna Beach</b><br>Popular tourist destination",
        icon=folium.Icon(color='blue', icon='tint')
    ).add_to(m)

    folium_static(m, width=800, height=500)

    st.markdown("""
    #### Key Geographic Features:
    - **Colombo**: Commercial capital and largest city
    - **Kandy**: Cultural capital and home to the Temple of the Tooth
    - **Central Highlands**: Mountainous region with tea plantations
    - **Northern Peninsula**: Jaffna and surrounding areas
    - **Eastern Coast**: Beautiful beaches and Trincomalee harbor
    """)

# Data explorer
def render_visualization(data, sort_order):
    st.markdown("## Data Visualization")
    chart_type = st.selectbox(
        "Chart Type",
        ["Line Chart", "Bar Chart", "Scatter Plot", "Box Plot"],
        key="viz_chart_type"
    )

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
    else:
        fig = px.box(
            data,
            x='Indicator Name',
            y='Value',
            color='Indicator Name',
            title="Statistical Distribution"
        )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        margin=dict(b=100)
    )

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("View Filtered Data"):
        st.dataframe(
            data.sort_values(
                ['Year', 'Value'],
                ascending=(sort_order == "Ascending")
            ),
            height=300
        )

def show_data_explorer(health_data):
    initialize_page("Data Explorer")
    st.markdown("## Data Explorer\nAdjust filters in the sidebar to update the visualization below.")

    if 'current_filters' not in st.session_state:
        st.warning("Please configure filters in the sidebar first.")
        return

    filters = st.session_state.current_filters

    filtered = health_data[
        (health_data['Year'].between(filters['year_range'][0], filters['year_range'][1])) &
        (health_data['Indicator Name'].isin(filters['indicators']))
    ]

    if filters.get('keyword') and filters['keyword'] != "All":
        filtered = filtered[filtered['Indicator Name'].str.contains(filters['keyword'], case=False)]

    if filters.get('category') and filters['category'] != "All":
        filtered = filtered[filtered['Category'] == filters['category']]

    if filtered.empty:
        st.warning("No data matches current filters. Try broadening your criteria.")
    else:
        render_visualization(filtered, filters.get('sort_order', "Ascending"))

# Forecasting
def show_forecasting(data):
    initialize_page("Forecasting")
    st.markdown("## Time Series Forecasting\nThis section provides basic ARIMA forecasting for selected health indicators.")

    if 'current_filters' not in st.session_state:
        st.warning("Please select indicators in the sidebar first.")
        return

    indicators = st.session_state.current_filters.get('indicators', [])
    if not indicators:
        st.warning("Please select at least one indicator in the sidebar.")
        return

    for indicator in indicators:
        st.subheader(f"Forecast for {indicator}")

        indicator_data = data[data['Indicator Name'] == indicator]
        if len(indicator_data) < 5:
            st.warning(f"Not enough data points for {indicator}. Need at least 5 years of data.")
            continue

        ts = indicator_data.set_index('Year')['Value'].sort_index()

        try:
            model = ARIMA(ts, order=(1, 1, 1))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=5)

            forecast_years = [ts.index.max() + i for i in range(1, 6)]
            forecast_df = pd.DataFrame({'Year': forecast_years, 'Forecasted Value': forecast.values})

            fig = px.line(forecast_df, x='Year', y='Forecasted Value', title=f"Forecast for {indicator}")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error forecasting {indicator}: {str(e)}")
