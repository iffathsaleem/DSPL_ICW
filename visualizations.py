import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def show_bullet_graph(health, indicator, target_value, year_range):

    st.subheader("Key Indicator - Bullet Graph")

    if not indicator:
        st.info("Please select an indicator from the sidebar to display the bullet graph.")
        return

    # Ensure the 'Value' column is numeric
    health['Value'] = pd.to_numeric(health['Value'], errors='coerce')

    # Filter the data
    indicator_data = health[
        (health['Indicator Name'] == indicator) & 
        (health['Year'].between(year_range[0], year_range[1]))
    ].dropna(subset=['Value', 'Year'])

    if indicator_data.empty:
        st.warning("No data available for the selected indicator and year range.")
        return

    # Group the data by year
    indicator_data = indicator_data.groupby('Year', as_index=False)['Value'].mean()

    for _, row in indicator_data.iterrows():
        actual = row['Value']
        year = row['Year']

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

        fig.update_layout(
            barmode='overlay',
            title=f"{indicator} ({int(year)})",
            xaxis=dict(title='Value'),
            yaxis=dict(title='Year'),
            height=200
        )

        st.plotly_chart(fig)

def show_radar_chart(health, category):
    
    st.subheader(f"Radar Chart: Indicator Comparison for {category}")
    category_data = health[health['Category'] == category]
    indicators = category_data['Indicator Name'].unique()

    if len(indicators) == 0:
        st.info("No indicators available in this category to display a radar chart.")
        return

    values = [category_data[category_data['Indicator Name'] == indicator]['Value'].mean() 
              for indicator in indicators]
    
    radar_data = pd.DataFrame({'Indicator': indicators, 'Value': values})
    fig = px.line_polar(radar_data, r='Value', theta='Indicator', line_close=True)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)

import plotly.express as px

def show_animated_line_chart(data):
    """Display an animated line chart of indicators over time"""
    if data.empty:
        st.warning("No data available for animation")
        return
    
    try:
        fig = px.line(
            data.sort_values('Year'),
            x='Year',
            y='Value',
            color='Indicator Name',
            animation_frame='Year',
            title='Health Indicators Over Time',
            labels={'Value': 'Value', 'Year': 'Year'},
            height=500
        )
        fig.update_layout(
            xaxis_range=[data['Year'].min(), data['Year'].max()],
            yaxis_range=[data['Value'].min()*0.9, data['Value'].max()*1.1],
            transition={'duration': 500}
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Animation error: {str(e)}")

def show_trend_chart(data, title, indicators):
    if data.empty:
        st.warning(f"No data available for {title}")
        return
    
    try:
        fig = px.line(
            data,
            x='Year',
            y='Value',
            color='Indicator Name',
            title=title,
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Chart error: {str(e)}")

def show_comparative_chart(data, indicators, title, color_map=None):

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
        title=title
    )
    
    fig.update_layout(
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
    
    st.plotly_chart(fig)

def show_pie_chart(data, category_name, relevant_indicators=None):
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
        st.plotly_chart(fig)

def show_stacked_area_chart(health):
    st.subheader("Category Contributions Over Time")
    fig = px.area(
        health, 
        x='Year', 
        y='Value', 
        color='Category', 
        line_group='Category',
        title="Area Chart of Categories"
    )
    st.plotly_chart(fig)

def show_distribution_charts(data):

    # Bar Chart of Indicator Frequency
    st.subheader("Indicator Frequency by Code")
    freq_data = data['Indicator_Code'].value_counts().reset_index()
    freq_data.columns = ['Indicator_Code', 'Count']
    fig_bar = px.bar(freq_data, x='Indicator_Code', y='Count', 
                    title="Frequency of Each Indicator (Code)")
    st.plotly_chart(fig_bar)
    
    # Line Chart of Total Values Over Time
    st.subheader("Total Indicator Values Over Time")
    trend_data = data.groupby('Year')['Value'].sum().reset_index()
    fig_line = px.line(trend_data, x='Year', y='Value', 
                      title="Trend of Total Indicator Values Over Time")
    st.plotly_chart(fig_line)
    
    # Histogram of Value Distribution
    st.subheader("Distribution of Indicator Values")
    fig_hist = px.histogram(data, x='Value', nbins=50, 
                           title="Distribution of All Indicator Values")
    st.plotly_chart(fig_hist)
    
    # Heatmap of Indicator Counts per Year
    st.subheader("Indicator Presence Heatmap (by Code and Year)")
    heatmap_data = data.groupby(['Year', 'Indicator_Code']).size().unstack(fill_value=0)
    fig_heat = px.imshow(heatmap_data.T, aspect='auto', 
                        title="Indicator Presence Over Years (by Code)")
    st.plotly_chart(fig_heat)
    
    # Donut Chart of Indicator Counts by Category
    st.subheader("Indicator Count by Category")
    category_counts = data['Category'].value_counts().reset_index()
    category_counts.columns = ["Category", "Count"]
    fig_donut = px.pie(category_counts, names="Category", values="Count", 
                       hole=0.5, title="Indicator Distribution by Category")
    st.plotly_chart(fig_donut)