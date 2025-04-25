import plotly.express as px
import streamlit as st
import pandas as pd

def show_trend_chart(data, title, indicators):
    """Display a static trend chart for specific indicators"""
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
            markers=True,
            labels={'Value': 'Value', 'Year': 'Year'}
        )
        fig.update_layout(
            height=500,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error generating chart: {str(e)}")

def show_bullet_graph(health, indicator, target_value, year_range):
    """Display a bullet graph for key indicators"""
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