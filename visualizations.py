import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from dashboard import initialize_page

# Initialize CSS
def initialize_visualization():
    st.markdown("""
    <style>
    .insight-card {
        background-color: rgba(30, 30, 30, 0.7);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# --- AUTOMATED INSIGHTS GENERATION (TextBlob removed) ---
def generate_chart_insights(data, chart_type, indicators=None):
    """Generate natural language insights about any chart"""
    insights = []
    
    if chart_type == "time_series":
        for indicator in indicators:
            ts_data = data[data['Indicator Name'] == indicator].set_index('Year')['Value']
            if len(ts_data) > 1:
                change_pct = ((ts_data[-1] - ts_data[0]) / ts_data[0]) * 100
                trend = "increased" if change_pct > 0 else "decreased"
                
                insight = f"""
                <div class='insight-card'>
                <b>{indicator}</b> {trend} by <b>{abs(change_pct):.1f}%</b> from {ts_data.index[0]} to {ts_data.index[-1]}. 
                {f'Peak value: {ts_data.max():.1f} in {ts_data.idxmax()}' if len(ts_data) > 3 else ''}
                </div>
                """
                insights.append(insight)
    
    elif chart_type == "correlation":
        corr_matrix = data.pivot_table(index='Year', columns='Indicator Name', values='Value').corr()
        strongest_pair = corr_matrix.unstack().sort_values(key=abs, ascending=False).index[1]
        val = corr_matrix.loc[strongest_pair[0], strongest_pair[1]]
        
        relationship = "strong positive" if val > 0.7 else "strong negative" if val < -0.7 else "moderate"
        insights.append(f"""
        <div class='insight-card'>
        <b>Strongest correlation</b>: {strongest_pair[0]} and {strongest_pair[1]} ({val:.2f})<br>
        This indicates a {relationship} relationship between these indicators.
        </div>
        """)
    
    return "".join(insights)

# --- ENHANCED FORECASTING ---
def show_time_series_forecast(data, indicator_name):
    ts_data = data[data['Indicator Name'] == indicator_name].set_index('Year')['Value'].dropna()
    
    # Insight generation
    st.markdown(generate_chart_insights(data, "time_series", [indicator_name]), unsafe_allow_html=True)
    
    if len(ts_data) < 5:
        show_linear_projection(data, indicator_name)
        return
    
    with st.spinner("Training forecasting model..."):
        try:
            model = ARIMA(ts_data, order=(1, 1, 1)).fit()
            forecast = model.forecast(steps=5)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=ts_data.index, y=ts_data, name='Historical'))
            fig.add_trace(go.Scatter(x=forecast.index, y=forecast, name='Forecast', line=dict(dash='dot')))
            fig.update_layout(title=f"Forecast for {indicator_name}", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            # Forecast insights
            forecast_change = ((forecast[-1] - ts_data[-1]) / ts_data[-1]) * 100
            st.markdown(f"""
            <div class='insight-card'>
            <b>Forecast Insight</b>: Predicted <b>{'increase' if forecast_change > 0 else 'decrease'}</b> of 
            <b>{abs(forecast_change):.1f}%</b> over the next 5 years.
            </div>
            """, unsafe_allow_html=True)
            
        except:
            show_linear_projection(data, indicator_name)

def show_linear_projection(data, indicator_name):
    """Fallback method when ARIMA fails"""
    ts_data = data[data['Indicator Name'] == indicator_name].set_index('Year')['Value'].dropna()
    
    if len(ts_data) >= 2:
        x = np.array(ts_data.index)
        y = ts_data.values
        coeffs = np.polyfit(x, y, 1)
        future_years = np.array([x[-1] + 1, x[-1] + 5])
        projected = coeffs[0] * future_years + coeffs[1]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, name='Historical'))
        fig.add_trace(go.Scatter(x=future_years, y=projected, name='Linear Projection', line=dict(dash='dot')))
        st.plotly_chart(fig, use_container_width=True)
        
        # Projection insight
        proj_change = ((projected[-1] - y[-1]) / y[-1]) * 100
        st.markdown(f"""
        <div class='insight-card'>
        <b>Linear Projection</b>: Based on simple trend, expecting <b>{'increase' if proj_change > 0 else 'decrease'}</b> 
        of <b>{abs(proj_change):.1f}%</b> in 5 years.
        </div>
        """, unsafe_allow_html=True)

# --- ENHANCED COMPARATIVE SECTION ---
def show_comparative_section(health_data):
    initialize_visualization()
    
    # Original controls
    available_indicators = sorted(health_data['Indicator Name'].unique())
    selected_indicators = st.multiselect("Select indicators", available_indicators, default=available_indicators[:2])
    
    if not selected_indicators:
        return
    
    filtered_data = health_data[health_data['Indicator Name'].isin(selected_indicators)]
    
    # Visualization selector
    chart_type = st.radio("Chart type", 
                         ["Trend Lines", "Small Multiples", "Correlation", "Forecast"],
                         horizontal=True)
    
    if chart_type == "Trend Lines":
        fig = px.line(filtered_data, x='Year', y='Value', color='Indicator Name')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(generate_chart_insights(filtered_data, "time_series", selected_indicators), unsafe_allow_html=True)
    
    elif chart_type == "Correlation" and len(selected_indicators) > 1:
        show_indicator_correlation(filtered_data, selected_indicators)
        st.markdown(generate_chart_insights(filtered_data, "correlation"), unsafe_allow_html=True)
    
    elif chart_type == "Forecast":
        indicator = st.selectbox("Select indicator to forecast", selected_indicators)
        show_time_series_forecast(filtered_data, indicator)

def show_indicator_correlation(data, indicators):
    """Enhanced correlation matrix with insights"""
    pivot_data = data.pivot_table(index='Year', columns='Indicator Name', values='Value')
    corr = pivot_data.corr()
    
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale='RdBu')
    st.plotly_chart(fig, use_container_width=True)

def show_interactive_map():
    """Standalone map function that doesn't depend on dashboard"""
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

# --- NEW VISUALIZATIONS (added enhancements) ---

def show_time_series_forecast(data, indicator_name):
    """Forecast future values using ARIMA"""
    ts_data = data[data['Indicator Name'] == indicator_name].set_index('Year')['Value'].dropna()
    
    if len(ts_data) < 5:
        st.warning("Insufficient data for forecasting (need ≥5 years).")
        return
    
    with st.spinner("Training forecasting model..."):
        model = ARIMA(ts_data, order=(1, 1, 1)).fit()
        forecast = model.forecast(steps=5)  # 5-year forecast
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ts_data.index, y=ts_data, 
        name='Historical Data',
        line=dict(width=3, color='#1f77b4')))
    fig.add_trace(go.Scatter(
        x=forecast.index, y=forecast, 
        name='Forecast',
        line=dict(dash='dot', color='red', width=3)))
    
    fig.update_layout(
        title=f"5-Year Forecast: {indicator_name}",
        xaxis_title="Year",
        yaxis_title="Value",
        template="plotly_dark",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_indicator_correlation(data, indicators):
    """Interactive correlation heatmap"""
    pivot_data = data.pivot_table(index='Year', columns='Indicator Name', values='Value')[indicators]
    corr = pivot_data.corr()
    
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale='RdBu',
        zmin=-1, zmax=1,
        title="Indicator Correlation Matrix"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_multi_indicator_trends(data, indicators):
    """Small multiples comparison"""
    fig = px.line(
        data[data['Indicator Name'].isin(indicators)],
        x='Year', y='Value',
        color='Indicator Name',
        facet_col='Indicator Name',
        facet_col_wrap=2,
        height=800,
        template="plotly_dark"
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def show_value_distribution(data, indicator_name):
    """Box plot + histogram"""
    filtered = data[data['Indicator Name'] == indicator_name]
    
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.box(filtered, y='Value', title=f"Distribution of {indicator_name}")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.histogram(filtered, x='Value', nbins=20, title="Value Frequency")
        st.plotly_chart(fig2, use_container_width=True)

# --- ENHANCED COMPARATIVE SECTION (updated but preserves original functionality) ---

def show_comparative_section(health_data):
    # Set the background first
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                   url('https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Trends%20Overtime.JPG');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .main .block-container {{
        background-color: rgba(30, 30, 30, 0.85) !important;
        border-radius: 10px;
        padding: 2rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
    }}
    </style>
    """, unsafe_allow_html=True)

    initialize_visualization()
    st.header("Comparative Insights")
    st.markdown("Compare multiple indicators over time using interactive charts.")
    
    # Get available indicators and years
    available_indicators = sorted(health_data['Indicator Name'].unique())
    min_year, max_year = int(health_data['Year'].min()), int(health_data['Year'].max())
    
    # Original control panel (unchanged)
    with st.expander("Comparison Settings", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            selected_indicators = st.multiselect(
                "Select indicators to compare",
                options=available_indicators,
                default=available_indicators[:2] if len(available_indicators) >= 2 else None,
                key="comp_insights_multiselect"
            )
        with col2:
            year_range = st.slider(
                "Year range",
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year),
                key="comp_insights_years"
            )
    
    if not selected_indicators:
        st.info("Please select at least one indicator to compare")
        return
    
    # Filter data (unchanged)
    filtered_data = health_data[
        (health_data['Indicator Name'].isin(selected_indicators)) &
        (health_data['Year'] >= year_range[0]) &
        (health_data['Year'] <= year_range[1])
    ]
    
    if filtered_data.empty:
        st.warning("No data available for the selected filters")
        return
    
    # Enhanced visualization selector
    st.subheader("Visualization Options")
    viz_type = st.radio(
        "Choose visualization type:",
        options=["Trend Lines", "Small Multiples", "Correlation", "Forecasting", "Distribution"],
        horizontal=True
    )
    
    if viz_type == "Trend Lines":
        # Original line/bar/area chart logic
        chart_type = st.radio(
            "Chart type",
            options=["Line Chart", "Bar Chart", "Area Chart"],
            horizontal=True
        )
        colors = px.colors.qualitative.Plotly
        color_map = {ind: colors[i % len(colors)] for i, ind in enumerate(selected_indicators)}
        
        if chart_type == "Line Chart":
            fig = px.line(filtered_data, x='Year', y='Value', color='Indicator Name', color_discrete_map=color_map)
        elif chart_type == "Bar Chart":
            fig = px.bar(filtered_data, x='Year', y='Value', color='Indicator Name', barmode='group', color_discrete_map=color_map)
        elif chart_type == "Area Chart":
            fig = px.area(filtered_data, x='Year', y='Value', color='Indicator Name', color_discrete_map=color_map)
        
        fig.update_layout(height=500, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
    elif viz_type == "Small Multiples":
        show_multi_indicator_trends(filtered_data, selected_indicators)
        
    elif viz_type == "Correlation":
        if len(selected_indicators) >= 2:
            show_indicator_correlation(filtered_data, selected_indicators)
        else:
            st.warning("Select at least 2 indicators for correlation analysis")
            
    elif viz_type == "Forecasting":
        indicator = st.selectbox("Select indicator to forecast", selected_indicators)
        show_time_series_forecast(filtered_data, indicator)
        
    elif viz_type == "Distribution":
        indicator = st.selectbox("Select indicator", selected_indicators)
        show_value_distribution(filtered_data, indicator)
    
    # Original statistical analysis section (unchanged)
    st.subheader("Statistical Analysis")
    with st.expander("View Detailed Statistics"):
        tab1, tab2 = st.tabs(["Summary Statistics", "Correlation Matrix"])
        with tab1:
            stats = filtered_data.groupby('Indicator Name')['Value'].describe()
            st.dataframe(stats.style.format("{:.2f}"))
        with tab2:
            if len(selected_indicators) > 1:
                pivot_data = filtered_data.pivot_table(index='Year', columns='Indicator Name', values='Value').corr()
                st.dataframe(pivot_data.style.format("{:.2f}").background_gradient(cmap='RdBu', vmin=-1, vmax=1))