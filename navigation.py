import streamlit as st

# Function for creating the horizontal navigation
def show_navigation():
    st.markdown("<h1 style='text-align: center;'>Sri Lanka Health Data Dashboard</h1>", unsafe_allow_html=True)
    navigation = st.radio("Select Section", [
        "Overview",
        "Trends Over Time",
        "Demographic Insights",
        "Expenditure Analysis",
        "Mortality Trends",
        "Key Indicator Highlights",
        "Comparative Insights"
    ], key="nav")

    return navigation
