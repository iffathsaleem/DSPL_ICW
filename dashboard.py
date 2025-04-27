import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc

# Set page config
st.set_page_config(page_title="Digital Sri Lanka Dashboard", layout="wide")

# Set sidebar background once
def set_sidebar_background():
    sidebar_style = """
    <style>
        [data-testid="stSidebar"] {
            background-image: url('https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/sidebar%20(1).jpg');
            background-size: cover;
        }
    </style>
    """
    st.markdown(sidebar_style, unsafe_allow_html=True)

set_sidebar_background()

# Set main background dynamically
def initialize_page(category_name):
    background_images = {
        "Digital Economy": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Digital%20Economy.jpg",
        "Digital Government": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Digital%20Government.jpg",
        "Digital Education": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Digital%20Education.jpg",
        "Digital Health": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Digital%20Health.jpg",
        "Digital Infrastructure": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Digital%20Infrastructure.jpg",
        "Cybersecurity and Data Protection": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Cybersecurity.jpg",
        "Digital Inclusion and Literacy": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Digital%20Inclusion.jpg",
        "Digital Laws and Regulations": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Laws.jpg",
        "Population Health and Demographics": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Demographic%20and%20Population.jpg", # newly added
    }

    background_image_url = background_images.get(category_name, "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/1.jpg")

    page_bg_style = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url('{background_image_url}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_style, unsafe_allow_html=True)

# Show animated overview
def show_overview(data):
    st.title("Overview of Key Indicators Over Time")

    available_indicators = list(data['Indicator'].unique())
    selected_indicators = st.multiselect('Select indicators to display:', available_indicators, default=available_indicators[:3])

    filtered_data = data[data['Indicator'].isin(selected_indicators)]

    colors = px.colors.qualitative.Plotly
    colors = (colors * ((len(available_indicators) // len(colors)) + 1))[:len(available_indicators)]

    fig = go.Figure()

    for i, indicator in enumerate(selected_indicators):
        indicator_data = filtered_data[filtered_data['Indicator'] == indicator]
        fig.add_trace(go.Scatter(
            x=indicator_data['Year'],
            y=indicator_data['Value'],
            mode='lines+markers',
            name=indicator,
            line=dict(color=colors[i])
        ))

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Value',
        title='Key Indicators Over Time',
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)

# General category analysis
def show_category_analysis(data, category_name):
    initialize_page(category_name)

    st.title(f"{category_name} Analysis")

    category_data = data[data['Category'] == category_name]

    if category_data.empty:
        st.warning("No data available for this category.")
        return

    show_overview(category_data)

    selected_year = st.selectbox('Select year to view specific insights:', sorted(category_data['Year'].unique(), reverse=True))
    year_data = category_data[category_data['Year'] == selected_year]

    st.subheader(f"{category_name} Insights for {selected_year}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Distribution of Indicators")
        fig = px.pie(year_data, names='Indicator', values='Value', title='Indicator Distribution')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Top Indicators")
        top_indicators = year_data.sort_values(by='Value', ascending=False).head(5)
        fig = px.bar(top_indicators, x='Value', y='Indicator', orientation='h', title='Top 5 Indicators')
        st.plotly_chart(fig, use_container_width=True)

# Define each section (no duplicates now!)
def show_digital_economy(data):
    show_category_analysis(data, "Digital Economy")

def show_digital_government(data):
    show_category_analysis(data, "Digital Government")

def show_digital_education(data):
    show_category_analysis(data, "Digital Education")

def show_digital_health(data):
    show_category_analysis(data, "Digital Health")

def show_digital_infrastructure(data):
    show_category_analysis(data, "Digital Infrastructure")

def show_cybersecurity_and_data_protection(data):
    show_category_analysis(data, "Cybersecurity and Data Protection")

def show_digital_inclusion_and_literacy(data):
    show_category_analysis(data, "Digital Inclusion and Literacy")

def show_digital_laws_and_regulations(data):
    show_category_analysis(data, "Digital Laws and Regulations")

def show_demographic_and_population_insights(data):
    show_category_analysis(data, "Population Health and Demographics")
