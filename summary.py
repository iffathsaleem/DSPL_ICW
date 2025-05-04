import streamlit as st
from dashboard import background_images

def show_summary():
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('{background_images["Executive Summary"]}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .block-container {{
            background-color: rgba(0, 0, 0, 0);
        }}
        h1, h2, h3, h4, h5, h6, p, li, div, .stMarkdown, .stText {{
            color: white !important;
        }}
        </style>
        """, unsafe_allow_html=True)
    
    st.title("Sri Lanka Health Executive Summary")
    
    st.markdown("""
    ## Major Trends (1960-2023)
    
    ### Achievements
    - Infant mortality reduced from 68 to 6 per 1,000 live births
    - Life expectancy increased from 62 to 77 years
    - 98% institutional delivery coverage achieved
    
    ### Ongoing Challenges
    - Rising non-communicable disease burden
    - Health workforce distribution disparities
    - Economic pressures on health financing
    
    ## Policy Implications
    1. **Prioritize** NCD prevention programs
    2. **Strengthen** primary healthcare networks
    3. **Optimize** health expenditure allocation
    """)
    
    cols = st.columns(3)
    with cols[0]:
        st.metric("Infant Mortality Rate", "6/1000", "-91% since 1960")
    with cols[1]:
        st.metric("Life Expectancy", "77 years", "+15 years since 1960")
    with cols[2]:
        st.metric("Health Expenditure", "3.5% of GDP", "Below WHO recommended 5%")
    