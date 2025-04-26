import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from categories import categories

# Background images configuration
background_images = {
    "About": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/About.jpg",
    "Overview": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Overview.jpg",
    "Population Health and Demographics": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Demographic%20Insights.jpg",
    "Health Expenditures": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Expenditure%20Analysis.jpg",
    "Mortality Rates": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Mortality%20%26%20Morbidity.jpg",
    "Comparative Insights": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Comparative%20Insights.jpg",
    "Key Indicator Highlights": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Key%20Indicator%20Highlights.jpg",
    "Maternal and Child Health": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Maternal%20and%20Child%20Health.jpg",
    "Infectious Diseases": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Infectious%20Diseases.jpg",
    "Nutrition and Food Security": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Nutrition%20and%20Food%20Security.jpg"
}

sidebar_image_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Sidebar.png"

def set_background(image_url):
    st.markdown(
        f"""
        <style>
            .stApp {{
                background: linear-gradient(
                    rgba(0, 0, 0, 0.7), 
                    rgba(0, 0, 0, 0.7)
                ), url("{image_url}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                color: white;
            }}
            .block-container {{
                background-color: rgba(0, 0, 0, 0);
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: white !important;
            }}
            .stMetric {{
                background-color: rgba(0, 0, 0, 0.5) !important;
                border-radius: 10px;
                padding: 10px;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

def set_sidebar_background(image_url):
    st.markdown(f"""
        <style>
            [data-testid="stSidebar"]::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: url('{image_url}');
                background-size: cover;
                background-position: center;
                opacity: 0.3;
                z-index: 0;
            }}
            [data-testid="stSidebar"]::after {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(255, 255, 255, 0.7);
                z-index: 1;
            }}
            [data-testid="stSidebar"] * {{
                position: relative;
                z-index: 2;
                color: black !important;
            }}
        </style>
    """, unsafe_allow_html=True)

def initialize_page(category):
    image_url = background_images.get(category)
    if image_url:
        set_background(image_url)
    set_sidebar_background(sidebar_image_url)
    st.title(f"{category}")

def format_value(value):
    if pd.isna(value):
        return "N/A"
    if isinstance(value, (int, float)):
        if value.is_integer():
            return f"{int(value):,}"
        return f"{value:,.2f}"
    return str(value)

def show_overview(health_data):
    initialize_page("Overview")
    
    health_data['Value'] = pd.to_numeric(health_data['Value'], errors='coerce')
    valid_data = health_data.dropna(subset=['Value'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dataset Summary")
        st.metric("Total Indicators", health_data['Indicator Name'].nunique())
        st.metric("Years Covered", f"{health_data['Year'].min()} to {health_data['Year'].max()}")
    
    with col2:
        st.subheader("Value Statistics")
        if not valid_data.empty:
            st.metric("Average Value", format_value(valid_data['Value'].mean()))
            st.metric("Data Points", len(valid_data))

    st.subheader("Interactive Category Trends")
    
    tabs = st.tabs(list(categories.keys()))
    for tab, (category, indicators) in zip(tabs, categories.items()):
        with tab:
            category_data = valid_data[valid_data['Indicator Name'].isin(indicators)]
            
            if not category_data.empty:
                fig = px.line(
                    category_data,
                    x='Year',
                    y='Value',
                    color='Indicator Name',
                    animation_frame='Year',
                    markers=True,
                    title=f'{category} Trends'
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=600,
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                with st.expander("View Raw Data"):
                    st.dataframe(
                        category_data[['Indicator Name', 'Year', 'Value']]
                        .sort_values(['Year', 'Indicator Name'])
                        .style.format({'Value': '{:,.2f}'}),
                        height=300
                    )
            else:
                st.warning(f"No data available for {category} indicators")

def show_category_analysis(data, category_name):
    """Focused analysis for a specific category"""
    initialize_page(category_name)
    indicators = categories.get(category_name, [])
    
    if not indicators:
        st.warning("No indicators defined for this category")
        return
    
    # Ensure numeric values
    data['Value'] = pd.to_numeric(data['Value'], errors='coerce')
    category_data = data[data['Indicator Name'].isin(indicators)].dropna(subset=['Value'])
    
    if not category_data.empty:
        # Comparative line chart
        st.subheader(f"{category_name} Trends")
        fig = px.line(
            category_data,
            x='Year',
            y='Value',
            color='Indicator Name',
            markers=True,
            title=f'Comparison of {category_name} Indicators'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Latest values summary
        st.subheader("Latest Values")
        latest_year = category_data['Year'].max()
        latest_data = category_data[category_data['Year'] == latest_year]
        
        cols = st.columns(3)
        for idx, (indicator, row) in enumerate(latest_data.iterrows()):
            cols[idx % 3].metric(
                label=row['Indicator Name'],
                value=format_value(row['Value']),
                help=f"Year: {latest_year}"
            )
    else:
        st.warning("No valid data available for selected indicators")

# Category-specific functions (all routed through show_category_analysis)
def show_demographic_and_population_insights(data): 
    show_category_analysis(data, "Population Health and Demographics")

def show_health_expenditure_insights(data): 
    show_category_analysis(data, "Health Expenditures")

def show_mortality_and_morbidity_trends(data): 
    show_category_analysis(data, "Mortality Rates")

def show_comparative_insights(data): 
    show_category_analysis(data, "Comparative Insights")

def show_key_indicator_highlights(data): 
    show_category_analysis(data, "Key Indicator Highlights")