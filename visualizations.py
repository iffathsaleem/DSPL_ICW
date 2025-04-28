import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
from statsmodels.tsa.arima.model import ARIMA

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

# Interactive map
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

def show_comparative_section(health_data):
    initialize_visualization()
    
    st.header("Comparative Insights")
    st.markdown("Compare multiple indicators over time using interactive charts.")
    
    # Get available indicators and years
    available_indicators = sorted(health_data['Indicator Name'].unique())
    min_year, max_year = int(health_data['Year'].min()), int(health_data['Year'].max())
    
    # Create controls
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
    
    # Filter data
    filtered_data = health_data[
        (health_data['Indicator Name'].isin(selected_indicators)) &
        (health_data['Year'] >= year_range[0]) &
        (health_data['Year'] <= year_range[1])
    ]
    
    if filtered_data.empty:
        st.warning("No data available for the selected filters")
        return
    
    # Visualization section
    st.subheader("Visual Comparison")
    
    # Enhanced chart type selection
    chart_type = st.radio(
        "Chart type",
        options=["Line Chart", "Bar Chart", "Area Chart", "Pie Chart", "Heatmap", "Scatter Plot", "Box Plot"],
        horizontal=True,
        key="comp_insights_chart_type"
    )
    
    colors = px.colors.qualitative.Plotly
    color_map = {ind: colors[i % len(colors)] for i, ind in enumerate(selected_indicators)}
    
    # Create charts based on selection
    if chart_type == "Line Chart":
        fig = px.line(
            filtered_data,
            x='Year',
            y='Value',
            color='Indicator Name',
            markers=True,
            color_discrete_map=color_map
        )
    elif chart_type == "Bar Chart":
        fig = px.bar(
            filtered_data,
            x='Year',
            y='Value',
            color='Indicator Name',
            barmode='group',
            color_discrete_map=color_map
        )
    elif chart_type == "Area Chart":
        fig = px.area(
            filtered_data,
            x='Year',
            y='Value',
            color='Indicator Name',
            line_group='Indicator Name',
            color_discrete_map=color_map
        )
    elif chart_type == "Pie Chart":
        latest_data = filtered_data[filtered_data['Year'] == max_year]
        fig = px.pie(
            latest_data,
            names='Indicator Name',
            values='Value',
            color='Indicator Name',
            color_discrete_map=color_map
        )
    elif chart_type == "Heatmap":
        pivot_data = filtered_data.pivot_table(
            index='Year',
            columns='Indicator Name',
            values='Value'
        )
        fig = px.imshow(
            pivot_data,
            labels=dict(x="Indicator", y="Year", color="Value"),
            aspect="auto"
        )
    elif chart_type == "Scatter Plot":
        if len(selected_indicators) >= 2:
            pivot_data = filtered_data.pivot_table(
                index='Year',
                columns='Indicator Name',
                values='Value'
            ).reset_index()
            fig = px.scatter(
                pivot_data,
                x=selected_indicators[0],
                y=selected_indicators[1],
                trendline="ols"
            )
        else:
            st.warning("Select at least 2 indicators for scatter plot")
            return
    elif chart_type == "Box Plot":
        fig = px.box(
            filtered_data,
            x='Indicator Name',
            y='Value',
            color='Indicator Name',
            color_discrete_map=color_map
        )
    
    # Add annotations for key insights
    if chart_type in ["Line Chart", "Bar Chart", "Area Chart"]:
        for indicator in selected_indicators:
            ind_data = filtered_data[filtered_data['Indicator Name'] == indicator]
            max_val = ind_data['Value'].max()
            min_val = ind_data['Value'].min()
            fig.add_annotation(
                x=ind_data[ind_data['Value'] == max_val]['Year'].values[0],
                y=max_val,
                text=f"Peak: {max_val:.2f}",
                showarrow=True,
                arrowhead=1
            )
            fig.add_annotation(
                x=ind_data[ind_data['Value'] == min_val]['Year'].values[0],
                y=min_val,
                text=f"Low: {min_val:.2f}",
                showarrow=True,
                arrowhead=1
            )
    
    fig.update_layout(
        height=500,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        margin=dict(b=100)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add key takeaways
    st.subheader("Key Takeaways")
    with st.expander("View Insights"):
        for indicator in selected_indicators:
            ind_data = filtered_data[filtered_data['Indicator Name'] == indicator]
            change = (ind_data['Value'].iloc[-1] - ind_data['Value'].iloc[0]) / ind_data['Value'].iloc[0] * 100
            st.write(f"**{indicator}**: Changed by {change:.1f}% from {year_range[0]} to {year_range[1]}")
    
    # Statistical comparison
    st.subheader("Statistical Analysis")
    with st.expander("View Detailed Statistics"):
        tab1, tab2 = st.tabs(["Summary Statistics", "Correlation Matrix"])
        
        with tab1:
            st.write("Descriptive statistics for selected indicators:")
            stats = filtered_data.groupby('Indicator Name')['Value'].describe()
            st.dataframe(stats.style.format("{:.2f}").background_gradient(cmap='Blues'))
        
        with tab2:
            if len(selected_indicators) > 1:
                try:
                    pivot_data = filtered_data.pivot_table(
                        index='Year',
                        columns='Indicator Name',
                        values='Value'
                    ).corr()
                    st.write("Correlation between indicators:")
                    st.dataframe(pivot_data.style.format("{:.2f}").background_gradient(
                        cmap='RdBu', vmin=-1, vmax=1))
                except Exception as e:
                    st.warning(f"Could not calculate correlation: {str(e)}")
            else:
                st.info("Select at least 2 indicators to see correlation analysis")