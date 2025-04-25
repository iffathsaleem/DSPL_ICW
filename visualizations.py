import plotly.express as px
import streamlit as st
import pandas as pd


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