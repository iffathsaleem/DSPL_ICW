import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from dashboard import background_images
from datetime import datetime

def initialize_visualization():
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('{background_images["Comparative Insights"]}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .main .block-container {{
        background-color: rgba(30, 30, 30, 0.85) !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
    }}
    .insight-card {{
        background-color: rgba(30, 30, 30, 0.7);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #4CAF50;
    }}
    </style>
    """, unsafe_allow_html=True)

def generate_chart_insights(data, chart_type, indicators=None):
    insights = []
    if chart_type == "time_series":
        for indicator in indicators:
            ts_data = data[data['Indicator Name'] == indicator].set_index('Year')['Value']
            if len(ts_data) > 1:
                try:
                    change_pct = ((ts_data.iloc[-1] - ts_data.iloc[0]) / ts_data.iloc[0]) * 100
                    trend = "increased" if change_pct > 0 else "decreased"
                    peak_val = f"Peak value: {ts_data.max():.1f} in {ts_data.idxmax()}" if len(ts_data) > 3 else ""
                    insight = f"""<div class='insight-card'><b>{indicator}</b> {trend} by <b>{abs(change_pct):.1f}%</b> from {ts_data.index[0]} to {ts_data.index[-1]}. {peak_val}</div>"""
                    insights.append(insight)
                except Exception:
                    insights.append(f"<div class='insight-card'>Insufficient data to analyze trend for {indicator}</div>")
            else:
                insights.append(f"<div class='insight-card'>Not enough data points to analyze trend for {indicator}</div>")
    if chart_type == "correlation":
        try:
            corr_matrix = data.pivot_table(index='Year', columns='Indicator Name', values='Value').corr()
            strongest_pair = corr_matrix.unstack().sort_values(key=abs, ascending=False).index[1]
            val = corr_matrix.loc[strongest_pair[0], strongest_pair[1]]
            relationship = "strong positive" if val > 0.7 else "strong negative" if val < -0.7 else "moderate"
            insights.append(f"""<div class='insight-card'><b>Strongest correlation</b>: {strongest_pair[0]} and {strongest_pair[1]} ({val:.2f})<br>This indicates a {relationship} relationship between these indicators.</div>""")
        except Exception:
            insights.append("<div class='insight-card'>Could not calculate correlations</div>")
    return "".join(insights)

def show_time_series_forecast(data, indicator_name):
    try:
        ts_data = data[data['Indicator Name'] == indicator_name].set_index('Year')['Value'].dropna()
        if len(ts_data) == 0:
            st.warning(f"No data available for {indicator_name}")
            return
        
        last_historical_year = ts_data.index.max()
        if last_historical_year < datetime.now().year - 2:
            st.info(f"Data current through {last_historical_year} (projecting {datetime.now().year - last_historical_year} years forward)")
        
        forecast_years = list(range(last_historical_year + 1, last_historical_year + 6))
        all_years = sorted(list(ts_data.index) + forecast_years)
        
        if len(ts_data) < 2:
            st.warning("Not enough data for forecasting")
            return
        
        with st.spinner("Generating forecast..."):
            try:
                model = ARIMA(ts_data, order=(1, 1, 1)).fit()
                forecast = model.get_forecast(steps=5)
                forecast_values = forecast.predicted_mean.values.tolist()
                
                if len(forecast_values) != 5:
                    forecast_values = [float(ts_data.iloc[-1])] * 5
                    
            except Exception:
                forecast_values = [float(ts_data.iloc[-1])] * 5
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=ts_data.index.tolist(),
                y=ts_data.values.tolist(),
                name='Historical Data',
                line=dict(width=4, color='#1f77b4'),
                marker=dict(size=8)
            ))
            fig.add_trace(go.Scatter(
                x=forecast_years,
                y=forecast_values,
                name='Forecast',
                line=dict(width=4, color='red', dash='dot'),
                marker=dict(size=8, symbol='diamond')
            ))
            
            fig.update_layout(
                title=f"{indicator_name} - Historical Trend & 5-Year Forecast",
                xaxis_title="Year",
                yaxis_title="Value",
                template="plotly_dark",
                font=dict(color="white", size=14),
                xaxis=dict(
                    tickmode='array',
                    tickvals=all_years[::max(1, len(all_years)//10)],
                    ticktext=[f"<b>{y}</b>" if y > last_historical_year else str(y) 
                            for y in all_years[::max(1, len(all_years)//10)]],
                    tickangle=0,
                    tickfont=dict(size=12),
                    showgrid=True,
                    gridwidth=0.5,
                    gridcolor='rgba(100,100,100,0.2)'
                ),
                yaxis=dict(
                    gridcolor='rgba(100,100,100,0.2)',
                    gridwidth=0.5
                ),
                hovermode="x unified",
                height=600,
                margin=dict(l=50, r=50, b=100, t=100),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    font=dict(size=12)
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            last_actual_value = float(ts_data.iloc[-1])
            last_forecast_value = forecast_values[-1]
            forecast_change = ((last_forecast_value - last_actual_value) / last_actual_value) * 100
            
            st.markdown(f"""
            <div style='
                background: rgba(30,30,30,0.8);
                border-radius: 10px;
                padding: 15px;
                margin: 15px 0;
                border-left: 4px solid #FF5722;
                font-size: 14px;
            '>
                <b style='font-size:16px'>Forecast Summary ({forecast_years[0]}-{forecast_years[-1]})</b><br>
                Predicted <b>{'increase' if forecast_change > 0 else 'decrease'}</b> of <b>{abs(forecast_change):.1f}%</b> from {last_historical_year}
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Forecast error: {str(e)}")
        show_linear_projection(data, indicator_name)

def show_linear_projection(data, indicator_name):
    try:
        ts_data = data[data['Indicator Name'] == indicator_name].set_index('Year')['Value'].dropna()
        if len(ts_data) >= 2:
            x = np.array(ts_data.index)
            y = ts_data.values
            coeffs = np.polyfit(x, y, 1)
            future_years = np.arange(x[-1] + 1, x[-1] + 6)
            projected = coeffs[0] * future_years + coeffs[1]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x,
                y=y,
                name='Historical',
                line=dict(width=4, color='#1f77b4'),
                mode='lines+markers'
            ))
            fig.add_trace(go.Scatter(
                x=future_years,
                y=projected,
                name='Projection',
                line=dict(width=4, color='red', dash='dot'),
                mode='lines+markers'
            ))
            
            fig.update_layout(
                title=f"{indicator_name} - 5 Year Projection",
                xaxis_title="Year",
                yaxis_title="Value",
                template="plotly_dark",
                font=dict(color="white", size=14),
                xaxis=dict(
                    tickmode='array',
                    tickvals=np.concatenate([x, future_years])[::max(1, len(x)//5)],
                    tickangle=45,
                    showgrid=True
                ),
                height=600,
                margin=dict(l=50, r=50, b=100, t=100)
            )
            
            st.plotly_chart(fig, use_container_width=True)

            proj_change = ((projected[-1] - y[-1]) / y[-1]) * 100
            st.markdown(f"""
            <div style='background:rgba(30,30,30,0.8);border-radius:10px;padding:15px;margin:10px 0;border-left:4px solid #FFA500'>
            <b>Projection Summary</b><br>
            Expected <b>{'increase' if proj_change > 0 else 'decrease'}</b> of <b>{abs(proj_change):.1f}%</b> by {int(future_years[-1])}
            </div>
            """, unsafe_allow_html=True)
            
    except Exception:
        st.error("Error generating projection")

def show_indicator_correlation(data, indicators):
    try:
        pivot_data = data.pivot_table(index='Year', columns='Indicator Name', values='Value')[indicators]
        corr = pivot_data.corr()
        fig = px.imshow(corr, text_auto=".2f", color_continuous_scale='RdBu', zmin=-1, zmax=1)
        fig.update_layout(template="plotly_dark", font=dict(color="white"))
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.error("Could not calculate correlations")

def show_multi_indicator_trends(data, indicators):
    try:
        fig = px.line(data[data['Indicator Name'].isin(indicators)], x='Year', y='Value', color='Indicator Name', facet_col='Indicator Name', facet_col_wrap=2, height=800)
        fig.update_layout(template="plotly_dark", showlegend=False, font=dict(color="white"))
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.error("Could not display trends")

def show_value_distribution(data, indicator_name):
    try:
        filtered = data[data['Indicator Name'] == indicator_name]
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.box(filtered, y='Value', title=f"Distribution of {indicator_name}")
            fig1.update_layout(template="plotly_dark", font=dict(color="white"))
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.histogram(filtered, x='Value', nbins=20, title="Value Frequency")
            fig2.update_layout(template="plotly_dark", font=dict(color="white"))
            st.plotly_chart(fig2, use_container_width=True)
    except Exception:
        st.error("Could not show distribution")

def show_comparative_section(health_data):
    initialize_visualization()
    st.header("Comparative Insights")
    
    available_indicators = sorted(health_data['Indicator Name'].unique())
    min_year, max_year = int(health_data['Year'].min()), int(health_data['Year'].max())
    
    with st.expander("Comparison Settings", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            selected_indicators = st.multiselect(
                "Select indicators to compare",
                options=available_indicators,
                default=available_indicators[:2] if len(available_indicators) >= 2 else None
            )
        with col2:
            year_range = st.slider(
                "Year range",
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year)
            )
    
    if not selected_indicators:
        st.info("Please select at least one indicator to compare")
        return
    
    filtered_data = health_data[
        (health_data['Indicator Name'].isin(selected_indicators)) &
        (health_data['Year'] >= year_range[0]) &
        (health_data['Year'] <= year_range[1])
    ]
    
    if filtered_data.empty:
        st.warning("No data available for the selected filters")
        return
    
    viz_type = st.radio(
        "Choose visualization type:",
        options=["Trend Lines", "Small Multiples", "Correlation", "Forecasting", "Distribution"],
        horizontal=True
    )
    
    if viz_type == "Trend Lines":
        chart_type = st.radio("Chart type", options=["Line Chart", "Bar Chart", "Area Chart"], horizontal=True)
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

def show_interactive_map():
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

    folium_static(m, width=800, height=500)