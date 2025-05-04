import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from datetime import datetime
from plotly.subplots import make_subplots
from scipy import stats
import base64

def create_plotly_theme():
    return {
        "template": "plotly_dark",
        "font": {"color": "white", "size": 14},
        "plot_bgcolor": "rgba(0,0,0,0)",
        "paper_bgcolor": "rgba(0,0,0,0)",
        "xaxis": {
            "tickfont": {"color": "white", "size": 12},
            "title_font": {"color": "white", "size": 16},
            "gridcolor": "rgba(255,255,255,0.1)",
            "zerolinecolor": "rgba(255,255,255,0.2)"
        },
        "yaxis": {
            "tickfont": {"color": "white", "size": 12},
            "title_font": {"color": "white", "size": 16},
            "gridcolor": "rgba(255,255,255,0.1)",
            "zerolinecolor": "rgba(255,255,255,0.2)"
        },
        "legend": {
            "font": {"color": "white", "size": 12},
            "bgcolor": "rgba(0,0,0,0.5)",
            "bordercolor": "rgba(255,255,255,0.2)"
        },
        "title": {
            "font": {"color": "white", "size": 20}
        },
        "margin": {"l": 50, "r": 50, "b": 50, "t": 80},
        "colorway": px.colors.qualitative.Plotly
    }

def get_bg_image_base64(image_url):
    import requests
    response = requests.get(image_url)
    return base64.b64encode(response.content).decode("utf-8")

def set_background_image(image_url):
    bg_img_base64 = get_bg_image_base64(image_url)
    
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """, unsafe_allow_html=True)

def initialize_visualization():
    st.markdown("""
    <style>
    .stApp {
        color: white;
    }
    .stMarkdown, .stText, .stHeader, .stSubheader {
        color: white !important;
        text-shadow: 0px 0px 5px rgba(0,0,0,0.8);
    }
    .stExpander {
        border-color: rgba(255, 255, 255, 0.2);
        background-color: rgba(0,0,0,0.7) !important;
        border-radius: 8px;
    }
    div[data-baseweb="select"] > div {
        color: white;
        background-color: rgba(0,0,0,0.7) !important;
    }
    .stPlotlyChart {
        background-color: rgba(0,0,0,0.7) !important;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .stRadio > div {
        background-color: rgba(0,0,0,0.7) !important;
        padding: 10px;
        border-radius: 8px;
    }
    .stRadio label {
        color: white !important;
        text-shadow: 0px 0px 4px rgba(0,0,0,0.8);
    }
    .stSlider > div {
        background-color: rgba(0,0,0,0.7) !important;
        padding: 15px;
        border-radius: 8px;
    }
    .stMultiSelect > div {
        background-color: rgba(0,0,0,0.7) !important;
        border-radius: 8px;
    }
    .st-br {
        padding-bottom: 10px;
    }
    .stSelectbox > div > div {
        background-color: rgba(0,0,0,0.7) !important;
        color: white;
    }
    .streamlit-expanderHeader {
        color: white !important;
        text-shadow: 0px 0px 4px rgba(0,0,0,0.8);
        background-color: rgba(0,0,0,0.7) !important;
        border-radius: 8px;
    }
    .stAlert {
        background-color: rgba(0,0,0,0.7) !important;
        color: white !important;
    }
    .stAlert > div {
        color: white !important;
    }
    div[data-testid="stToolbar"] {
        background-color: rgba(0,0,0,0.7) !important;
        border-radius: 8px;
    }
    .stButton > button {
        background-color: rgba(0,0,0,0.7) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
    }
    .stButton > button:hover {
        border: 1px solid rgba(255,255,255,0.5) !important;
    }
    div[data-baseweb="tab-list"] {
        background-color: rgba(0,0,0,0.7) !important;
        border-radius: 8px;
    }
    div[data-baseweb="tab"] {
        color: white !important;
    }
    .css-1y4p8pa {
        max-width: 1200px !important;
    }
    .css-1oe6wy4 {
        background-color: rgba(0,0,0,0.7) !important;
        padding: 30px !important;
        border-radius: 10px !important;
    }
    .stWarning, .stInfo, .stSuccess, .stError {
        background-color: rgba(0,0,0,0.7) !important;
        color: white !important;
        text-shadow: 0px 0px 4px rgba(0,0,0,0.8);
    }
    </style>
    """, unsafe_allow_html=True)

def generate_chart_insights(data, chart_type, indicators=None):
    insights = []
    
    if chart_type == "time_series" and indicators:
        for indicator in indicators:
            indicator_data = data[data['Indicator Name'] == indicator]
            
            if not indicator_data.empty:
                sorted_data = indicator_data.sort_values('Year')
                start_year = sorted_data['Year'].min()
                end_year = sorted_data['Year'].max()
                start_value = sorted_data[sorted_data['Year'] == start_year]['Value'].values[0]
                end_value = sorted_data[sorted_data['Year'] == end_year]['Value'].values[0]
                
                change = end_value - start_value
                percent_change = (change / start_value * 100) if start_value != 0 else float('inf')
                
                trend_direction = "increased" if change > 0 else "decreased" if change < 0 else "remained stable"
                
                insight = f"""
                <div style="color: white; text-shadow: 0px 0px 4px rgba(0,0,0,0.9); background-color: rgba(0,0,0,0.7); padding: 15px; border-radius: 8px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                  <strong>{indicator}</strong> {trend_direction} by <span style="color: {'#81D4FA' if change > 0 else '#FF8A65' if change < 0 else '#FFFFFF'}">{abs(percent_change):.1f}%</span> from {int(start_year)} to {int(end_year)}.
                  <br>Peak value: <span style="color: #AED581">{sorted_data['Value'].max():.1f}</span> in {int(sorted_data.loc[sorted_data['Value'].idxmax()]['Year'])}
                </div>
                """
                insights.append(insight)
    
    elif chart_type == "correlation" and len(data['Indicator Name'].unique()) >= 2:
        try:
            pivot_data = data.pivot_table(index='Year', columns='Indicator Name', values='Value')
            correlation_matrix = pivot_data.corr()
            
            corr_pairs = []
            for i in range(len(correlation_matrix.columns)):
                for j in range(i+1, len(correlation_matrix.columns)):
                    indicator1 = correlation_matrix.columns[i]
                    indicator2 = correlation_matrix.columns[j]
                    corr_value = correlation_matrix.iloc[i, j]
                    corr_pairs.append((indicator1, indicator2, corr_value))
            
            if corr_pairs:
                corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
                top_pair = corr_pairs[0]
                
                relationship = "positive" if top_pair[2] > 0 else "negative"
                strength = "strong" if abs(top_pair[2]) > 0.7 else "moderate" if abs(top_pair[2]) > 0.3 else "weak"
                
                # Determine color based on correlation strength and type
                corr_color = "#81D4FA" if top_pair[2] > 0 else "#FF8A65"  # Blue for positive, orange for negative
                
                insight = f"""
                <div style="color: white; text-shadow: 0px 0px 4px rgba(0,0,0,0.9); background-color: rgba(0,0,0,0.7); padding: 15px; border-radius: 8px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                  <strong>Strongest correlation:</strong> <span style="color: #E1BEE7">{top_pair[0]}</span> and <span style="color: #E1BEE7">{top_pair[1]}</span> (<span style="color: {corr_color}">{top_pair[2]:.2f}</span>)<br>
                  This indicates a <span style="color: {'#AED581' if abs(top_pair[2]) > 0.7 else '#FFAB40' if abs(top_pair[2]) > 0.3 else '#BDBDBD'}">{strength}</span> {relationship} relationship between these indicators.
                </div>
                """
                insights.append(insight)
        except Exception:
            insights.append("""
            <div style="color: white; text-shadow: 0px 0px 4px rgba(0,0,0,0.9); background-color: rgba(0,0,0,0.7); padding: 15px; border-radius: 8px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
              <strong>Analysis Note:</strong> Could not calculate correlations with the current data selection.
            </div>
            """)
    
    return "".join(insights)

def show_time_series_forecast(data, indicator_name):
    try:
        ts_data = data[data['Indicator Name'] == indicator_name].set_index('Year')['Value'].dropna()
        if len(ts_data) < 2:
            st.warning(f"Not enough data for forecasting {indicator_name}")
            return
        
        ts_data = ts_data.sort_index()
        
        last_historical_year = ts_data.index.max()
        forecast_years = list(range(last_historical_year + 1, last_historical_year + 6))
        all_years = sorted(list(ts_data.index) + forecast_years)
        
        try:
            model = ARIMA(ts_data, order=(1, 1, 1)).fit()
            forecast = model.get_forecast(steps=5)
            forecast_values = forecast.predicted_mean.values.tolist()
            
            if len(forecast_values) != 5:
                forecast_values = [float(ts_data.iloc[-1])] * 5
                
        except Exception:
            x = np.array(ts_data.index)
            y = ts_data.values
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            forecast_values = [slope * year + intercept for year in forecast_years]
        
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
        
        theme = create_plotly_theme()
        fig.update_layout(
            title=f"{indicator_name} - Historical Trend & 5-Year Forecast",
            xaxis_title="Year",
            yaxis_title="Value",
            template=theme["template"],
            font=theme["font"],
            plot_bgcolor=theme["plot_bgcolor"],
            paper_bgcolor=theme["paper_bgcolor"],
            xaxis=dict(
                tickmode='array',
                tickvals=all_years[::max(1, len(all_years)//10)],
                ticktext=[str(y) for y in all_years[::max(1, len(all_years)//10)]],
                tickangle=0,
                tickfont=theme["xaxis"]["tickfont"],
                showgrid=True,
                gridwidth=0.5,
                gridcolor=theme["xaxis"]["gridcolor"],
                title_font=theme["xaxis"]["title_font"]
            ),
            yaxis=dict(
                gridcolor=theme["yaxis"]["gridcolor"],
                gridwidth=0.5,
                tickfont=theme["yaxis"]["tickfont"],
                title_font=theme["yaxis"]["title_font"]
            ),
            hovermode="x unified",
            height=600,
            margin=theme["margin"],
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=theme["legend"]["font"],
                bgcolor=theme["legend"]["bgcolor"]
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        last_actual_value = float(ts_data.iloc[-1])
        last_forecast_value = forecast_values[-1]
        forecast_change = ((last_forecast_value - last_actual_value) / last_actual_value) * 100
        
        # Choose color based on direction of change
        change_color = "#81D4FA" if forecast_change > 0 else "#FF8A65"
        
        st.markdown(f"""
        <div style="background-color: rgba(0,0,0,0.7); padding: 20px; border-radius: 8px; color: white; text-shadow: 0px 0px 4px rgba(0,0,0,0.8); box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
            <h3 style="margin-top: 0;">Forecast Summary ({forecast_years[0]}-{forecast_years[-1]})</h3>
            <p>Predicted <span style="color: {change_color}">{'increase' if forecast_change > 0 else 'decrease'} of {abs(forecast_change):.1f}%</span> from {last_historical_year}</p>
            <p style="font-size: 0.9em; opacity: 0.8;">Final forecasted value: {last_forecast_value:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error generating forecast: {str(e)}")

def show_indicator_correlation(data, indicators):
    try:
        pivot_data = data.pivot_table(index='Year', columns='Indicator Name', values='Value')[indicators]
        corr = pivot_data.corr()
        
        theme = create_plotly_theme()
        
        fig = px.imshow(
            corr, 
            text_auto=".2f", 
            color_continuous_scale='RdBu', 
            zmin=-1, 
            zmax=1
        )
        
        fig.update_layout(
            template=theme["template"],
            font=theme["font"],
            plot_bgcolor=theme["plot_bgcolor"],
            paper_bgcolor=theme["paper_bgcolor"],
            coloraxis=dict(colorbar=dict(tickfont=dict(color="white"))),
            title="Indicator Correlation Matrix",
            title_font=theme["title"]["font"]
        )
        
        for annotation in fig.layout.annotations:
            annotation.font.color = "white"
            
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Could not calculate correlations: {str(e)}")

def show_multi_indicator_trends(data, indicators):
    try:
        theme = create_plotly_theme()
        
        n_indicators = len(indicators)
        n_cols = min(2, n_indicators)
        n_rows = (n_indicators + n_cols - 1) // n_cols
        
        fig = make_subplots(
            rows=n_rows, 
            cols=n_cols,
            subplot_titles=indicators,
            vertical_spacing=0.1
        )
        
        for i, indicator in enumerate(indicators):
            row = i // n_cols + 1
            col = i % n_cols + 1
            
            indicator_data = data[data['Indicator Name'] == indicator].sort_values('Year')
            
            fig.add_trace(
                go.Scatter(
                    x=indicator_data['Year'], 
                    y=indicator_data['Value'],
                    mode='lines+markers',
                    name=indicator,
                    line=dict(width=3),
                    marker=dict(size=8)
                ),
                row=row, col=col
            )
            
            fig.update_xaxes(
                title_text='Year', 
                row=row, col=col,
                gridcolor=theme["xaxis"]["gridcolor"],
                tickfont=theme["xaxis"]["tickfont"]
            )
            
            fig.update_yaxes(
                title_text='Value', 
                row=row, col=col,
                gridcolor=theme["yaxis"]["gridcolor"],
                tickfont=theme["yaxis"]["tickfont"]
            )
        
        fig.update_layout(
            height=300 * n_rows,
            template=theme["template"],
            font=theme["font"],
            plot_bgcolor=theme["plot_bgcolor"],
            paper_bgcolor=theme["paper_bgcolor"],
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Could not display trends: {str(e)}")

def show_value_distribution(data, indicator_name):
    try:
        filtered = data[data['Indicator Name'] == indicator_name]
        theme = create_plotly_theme()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.box(
                filtered, 
                y='Value', 
                title=f"Distribution of {indicator_name}"
            )
            
            fig1.update_layout(
                template=theme["template"],
                font=theme["font"],
                plot_bgcolor=theme["plot_bgcolor"],
                paper_bgcolor=theme["paper_bgcolor"],
                yaxis=dict(
                    tickfont=theme["yaxis"]["tickfont"],
                    title_font=theme["yaxis"]["title_font"],
                    gridcolor=theme["yaxis"]["gridcolor"]
                ),
                xaxis=dict(
                    tickfont=theme["xaxis"]["tickfont"],
                    title_font=theme["xaxis"]["title_font"],
                    gridcolor=theme["xaxis"]["gridcolor"]
                ),
                title_font=theme["title"]["font"]
            )
            
            st.plotly_chart(fig1, use_container_width=True)
            
        with col2:
            fig2 = px.histogram(
                filtered, 
                x='Value', 
                nbins=20, 
                title="Value Frequency"
            )
            
            fig2.update_layout(
                template=theme["template"],
                font=theme["font"],
                plot_bgcolor=theme["plot_bgcolor"],
                paper_bgcolor=theme["paper_bgcolor"],
                yaxis=dict(
                    tickfont=theme["yaxis"]["tickfont"],
                    title_font=theme["yaxis"]["title_font"],
                    gridcolor=theme["yaxis"]["gridcolor"]
                ),
                xaxis=dict(
                    tickfont=theme["xaxis"]["tickfont"],
                    title_font=theme["xaxis"]["title_font"],
                    gridcolor=theme["xaxis"]["gridcolor"]
                ),
                title_font=theme["title"]["font"]
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
        st.markdown(f"""
        <div style="background-color: rgba(0,0,0,0.7); padding: 20px; border-radius: 8px; color: white; text-shadow: 0px 0px 4px rgba(0,0,0,0.8); box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
            <h3 style="margin-top: 0;">Distribution Summary</h3>
            <table style="width: 100%;">
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);"><strong>Mean:</strong></td>
                    <td style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);">{filtered['Value'].mean():.2f}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);"><strong>Median:</strong></td>
                    <td style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);">{filtered['Value'].median():.2f}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);"><strong>Standard Deviation:</strong></td>
                    <td style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);">{filtered['Value'].std():.2f}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Range:</strong></td>
                    <td style="padding: 8px;">{filtered['Value'].min():.2f} to {filtered['Value'].max():.2f}</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Could not show distribution: {str(e)}")

def show_comparative_section(health_data):
    initialize_visualization()
    
    comparative_bg_img = 'https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Comparative%20Insights.jpg'
    set_background_image(comparative_bg_img)
    
    available_indicators = sorted(health_data['Indicator Name'].unique())
    min_year, max_year = int(health_data['Year'].min()), int(health_data['Year'].max())
    
    st.markdown("""
    <div style="background-color: rgba(0,0,0,0.7); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style='color: white; text-shadow: 0px 0px 8px rgba(0,0,0,0.9); margin: 0;'>Comparative Insights</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: rgba(0,0,0,0.7); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style='color: white; text-shadow: 0px 0px 5px rgba(0,0,0,0.9); margin-top: 0;'>Comparison Settings</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div style='background-color: rgba(0,0,0,0.7); padding: 10px; border-radius: 8px;'><p style='color: white; text-shadow: 0px 0px 4px rgba(0,0,0,0.9); margin: 0 0 5px 0;'>Select indicators to compare</p></div>", unsafe_allow_html=True)
        selected_indicators = st.multiselect(
            "Select indicators to compare",
            options=available_indicators,
            default=available_indicators[:2] if len(available_indicators) >= 2 else None,
            label_visibility="collapsed"
        )
    with col2:
        st.markdown("<div style='background-color: rgba(0,0,0,0.7); padding: 10px; border-radius: 8px;'><p style='color: white; text-shadow: 0px 0px 4px rgba(0,0,0,0.9); margin: 0 0 5px 0;'>Year range</p></div>", unsafe_allow_html=True)
        year_range = st.slider(
            "Year range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            label_visibility="collapsed"
        )
    
    if not selected_indicators:
        st.markdown("""
        <div style="background-color: rgba(0,0,0,0.7); padding: 15px; border-radius: 10px;">
            <p style="color: #81D4FA; text-shadow: 0px 0px 4px rgba(0,0,0,0.9); margin: 0;">
                Please select at least one indicator to compare
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    filtered_data = health_data[
        (health_data['Indicator Name'].isin(selected_indicators)) &
        (health_data['Year'] >= year_range[0]) &
        (health_data['Year'] <= year_range[1])
    ]
    
    if filtered_data.empty:
        st.markdown("""
        <div style="background-color: rgba(0,0,0,0.7); padding: 15px; border-radius: 10px;">
            <p style="color: #FFD54F; text-shadow: 0px 0px 4px rgba(0,0,0,0.9); margin: 0;">
                No data available for the selected filters
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown("""
    <div style="background-color: rgba(0,0,0,0.7); padding: 10px; border-radius: 10px; margin-bottom: 15px;">
        <p style='color: white; text-shadow: 0px 0px 4px rgba(0,0,0,0.9); margin: 0;'>Choose visualization type:</p>
    </div>
    """, unsafe_allow_html=True)
    
    viz_type = st.radio(
        "Choose visualization type:",
        options=["Trend Lines", "Small Multiples", "Correlation", "Forecasting", "Distribution"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    if viz_type == "Trend Lines":
        theme = create_plotly_theme()
        
        fig = px.line(
            filtered_data, 
            x='Year', 
            y='Value', 
            color='Indicator Name',
            markers=True
        )
        
        fig.update_layout(
            height=500,
            template=theme["template"],
            font=theme["font"],
            plot_bgcolor=theme["plot_bgcolor"],
            paper_bgcolor=theme["paper_bgcolor"],
            xaxis=theme["xaxis"],
            yaxis=theme["yaxis"],
            legend=theme["legend"]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div style="background-color: rgba(0,0,0,0.7); padding: 10px; border-radius: 10px; margin-bottom: 15px;">
            <h3 style='color: white; text-shadow: 0px 0px 8px rgba(0,0,0,0.9); margin: 0;'>Trend Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        insights = generate_chart_insights(filtered_data, "time_series", selected_indicators)
        st.markdown(insights, unsafe_allow_html=True)
        
    elif viz_type == "Small Multiples":
        show_multi_indicator_trends(filtered_data, selected_indicators)
        
        st.markdown("<h3 style='color: white; text-shadow: 0px 0px 8px rgba(0,0,0,0.9);'>Multi-Indicator Analysis</h3>", unsafe_allow_html=True)
        insights = generate_chart_insights(filtered_data, "time_series", selected_indicators)
        st.markdown(insights, unsafe_allow_html=True)
        
    elif viz_type == "Correlation":
        if len(selected_indicators) >= 2:
            try:
                pivot_data = filtered_data.pivot_table(index='Year', columns='Indicator Name', values='Value')[selected_indicators]
                corr = pivot_data.corr()
                
                theme = create_plotly_theme()
                
                fig = px.imshow(
                    corr, 
                    text_auto=".2f", 
                    color_continuous_scale='RdBu', 
                    zmin=-1, 
                    zmax=1,
                    title="Indicator Correlation Matrix"
                )
                
                fig.update_layout(
                    template=theme["template"],
                    font=theme["font"],
                    plot_bgcolor=theme["plot_bgcolor"],
                    paper_bgcolor=theme["paper_bgcolor"],
                    coloraxis=dict(colorbar=dict(tickfont=dict(color="white"))),
                    title_font=theme["title"]["font"]
                )
                
                for annotation in fig.layout.annotations:
                    annotation.font.color = "white"
                    
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("""
                <div style="background-color: rgba(0,0,0,0.7); padding: 10px; border-radius: 10px; margin-bottom: 15px;">
                    <h3 style='color: white; text-shadow: 0px 0px 8px rgba(0,0,0,0.9); margin: 0;'>Correlation Analysis</h3>
                </div>
                """, unsafe_allow_html=True)
                
                insights = generate_chart_insights(filtered_data, "correlation")
                st.markdown(insights, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Could not generate correlation matrix: {str(e)}")
        else:
            st.warning("Select at least 2 indicators for correlation analysis")
            
    elif viz_type == "Forecasting":
        indicator = st.selectbox("Select indicator to forecast", selected_indicators)
        show_time_series_forecast(filtered_data, indicator)
        
    elif viz_type == "Distribution":
        indicator = st.selectbox("Select indicator", selected_indicators)
        indicator_data = filtered_data[filtered_data['Indicator Name'] == indicator]
        
        if not indicator_data.empty:
            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2, gap="large")
            
            with col1:
                fig1 = px.box(
                    indicator_data,
                    y='Value',
                    title=f"<b>Box Plot of {indicator}</b>",
                    color_discrete_sequence=['#1f77b4']
                )
                fig1.update_layout(
                    template="plotly_dark",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    yaxis_title="Value",
                    showlegend=False,
                    margin=dict(l=50, r=50, t=60, b=50),
                    height=400
                )
                st.plotly_chart(fig1, use_container_width=True)
                
            with col2:
                fig2 = px.histogram(
                    indicator_data,
                    x='Value',
                    nbins=20,
                    title=f"<b>Distribution of {indicator}</b>",
                    color_discrete_sequence=['#1f77b4']
                )
                fig2.update_layout(
                    template="plotly_dark",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_title="Value",
                    yaxis_title="Count",
                    showlegend=False,
                    margin=dict(l=50, r=50, t=60, b=50),
                    height=400
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
            
            values = indicator_data['Value']
            stats = {
                "Mean": values.mean(),
                "Median": values.median(),
                "Std Dev": values.std(),
                "Min": values.min(),
                "Max": values.max(),
                "Count": len(values)
            }
            
            st.markdown(f"""
            <div style="background-color: rgba(0,0,0,0.7); 
                        padding: 20px; 
                        border-radius: 8px; 
                        color: white; 
                        text-shadow: 0px 0px 4px rgba(0,0,0,0.8); 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.2); 
                        margin-top: 20px;
                        margin-bottom: 20px;">
                <h3 style="margin-top: 0;">Distribution Summary for {indicator}</h3>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);"><strong>Mean:</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);">{stats['Mean']:.2f}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);"><strong>Median:</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);">{stats['Median']:.2f}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);"><strong>Std Dev:</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);">{stats['Std Dev']:.2f}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);"><strong>Min:</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);">{stats['Min']:.2f}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);"><strong>Max:</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);">{stats['Max']:.2f}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px;"><strong>Count:</strong></td>
                        <td style="padding: 8px;">{stats['Count']}</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning(f"No data available for {indicator} in the selected range")

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
            popup=f"{city['name']}\n{city['pop']}",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
        
    folium_static(m, width=800, height=500)