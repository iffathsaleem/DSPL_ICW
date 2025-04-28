import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from categories import categories
# Background image configuration
background_images = {
    "About": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/About.jpg",
    "Overview": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Overview.jpg",
    "Health Expenditure Insights": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Expenditure%20Analysis.jpg",
    "Mortality and Morbidity Trends": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Mortality%20%26%20Morbidity.jpg",
    "Comparative Insights": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Comparative%20Insights.jpg",
    "Key Indicator Highlights": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Key%20Indicator%20Highlights.jpg",
    "Maternal and Child Health": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Maternal%20and%20Child%20Health.jpg",
    "Infectious Diseases": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Infectious%20Diseases.jpg",
    "Nutrition and Food Security": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Nutrition%20and%20Food%20Security.jpg"
}

sidebar_image_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Sidebar.png"

# Fix the set_sidebar_background function
def set_sidebar_background(image_url):
    st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{
        position: relative;
    }}
    
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

    [data-testid="stSidebar"] > * {{
        position: relative;
        z-index: 2;
    }}

    /* SELECTION BOX STYLES - ORANGE WITH BLACK TEXT */
    div[data-baseweb="select"] [aria-selected="true"],
    div[data-baseweb="select"] [aria-selected="true"]:hover {{
        background-color: #FFA500 !important;  /* Orange background */
        color: #000000 !important;             /* Black text */
        font-weight: bold !important;
    }}

    /* Dropdown options */
    div[data-baseweb="select"] [role="option"] {{
        color: #000000 !important;
    }}

    /* Hover states for dropdown options */
    div[data-baseweb="select"] [role="option"]:hover {{
        background-color: #FFD699 !important;  /* Lighter orange */
        color: #000000 !important;
    }}

    /* Radio buttons and other selectors */
    div[data-baseweb="radio"] [aria-checked="true"] {{
        background-color: #FFA500 !important;
        color: #000000 !important;
        font-weight: bold !important;
    }}

    /* General text and labels */
    .st-emotion-cache-1v0mbdj,
    .stMarkdown, 
    .stText {{
        color: #000000 !important;
        font-weight: 500 !important;
    }}

    /* Input fields */
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #000000 !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    
def set_background(image_url):
    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url('{image_url}');
                background-size: cover;
                background-position: center;
            }}
            .overlay::before {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.7);
                z-index: 0;
            }}
        </style>
        <div class="overlay"></div>
    """, unsafe_allow_html=True)

def initialize_page(category):
    image_url = background_images.get(category, None)
    if image_url:
        set_background(image_url)
    set_sidebar_background(sidebar_image_url)
    st.title(f"{category} Analysis")

def format_value(value, is_percentage=False):
    """Format numbers consistently, handling percentages if specified."""
    if pd.isna(value):
        return "N/A"
    
    if is_percentage:
        return f"{value:.2f}%"
    
    if isinstance(value, (int, float)) and float(value).is_integer():
        return f"{int(value):,}"
    
    return f"{value:,.2f}"

def show_overview(health_data):
    initialize_page("Overview")
    
    # Basic statistics
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dataset Summary")
        st.metric("Total Indicators", health_data['Indicator Name'].nunique())
        st.metric("Years Covered", f"{health_data['Year'].min()} to {health_data['Year'].max()}")
    
    with col2:
        st.subheader("Value Statistics")
        health_data['Value'] = pd.to_numeric(health_data['Value'], errors='coerce')
        st.metric("Average Value", f"{health_data['Value'].mean():.2f}")
        st.metric("Data Points", len(health_data.dropna(subset=['Value'])))

    # Show animated charts for each category
    st.subheader("Category Trends Animation")
    
    # Create tabs for each major category
    tabs = st.tabs(list(categories.keys()))
    
    for tab, (category, indicators) in zip(tabs, categories.items()):
        with tab:
            # Filter data for this category
            category_data = health_data[
                (health_data['Indicator Name'].isin(indicators)) &
                (health_data['Value'].notna())
            ].copy()
            
            if not category_data.empty:
                # Get all available indicators in this category
                available_indicators = category_data['Indicator Name'].unique()
                
                st.write(f"Showing {len(available_indicators)} of {len(indicators)} indicators for {category}")
                
                # Create color sequence for all indicators
                colors = px.colors.qualitative.Plotly
                if len(available_indicators) > len(colors):
                    colors = colors * (len(available_indicators) // len(colors) + 1)
                
                # Create figure
                fig = go.Figure()
                
                # Add trace for each indicator
                for i, indicator in enumerate(available_indicators):
                    indicator_data = category_data[category_data['Indicator Name'] == indicator]
                    fig.add_trace(go.Scatter(
                        x=indicator_data['Year'],
                        y=indicator_data['Value'],
                        name=indicator,
                        mode='lines+markers',
                        marker=dict(size=8),
                        line=dict(width=3),
                        marker_color=colors[i],
                        line_color=colors[i]
                    ))
                
                # Animation frames
                frames = []
                years = sorted(category_data['Year'].unique())
                
                for year in years:
                    frame_data = category_data[category_data['Year'] <= year]
                    frames.append(go.Frame(
                        data=[
                            go.Scatter(
                                x=frame_data[frame_data['Indicator Name'] == ind]['Year'],
                                y=frame_data[frame_data['Indicator Name'] == ind]['Value'],
                                mode='lines+markers'
                            ) for ind in available_indicators
                        ],
                        name=str(year)
                    ))
                
                # Add frames to figure
                fig.frames = frames
                
                # Animation controls
                fig.update_layout(
                    updatemenus=[dict(
                        type="buttons",
                        buttons=[
                            dict(
                                label="▶ Play",
                                method="animate",
                                args=[None, {"frame": {"duration": 500, "redraw": True}, 
                                            "fromcurrent": True, "transition": {"duration": 300}}]
                            ),
                            dict(
                                label="❚❚ Pause",
                                method="animate",
                                args=[[None], {"frame": {"duration": 0, "redraw": False}, 
                                              "mode": "immediate", "transition": {"duration": 0}}]
                            )
                        ],
                        direction="left",
                        pad={"r": 10, "t": 87},
                        x=0.1,
                        y=0
                    )],
                    xaxis=dict(
                        range=[category_data['Year'].min()-1, category_data['Year'].max()+1],
                        title='Year'
                    ),
                    yaxis=dict(
                        range=[category_data['Value'].min()*0.9, category_data['Value'].max()*1.1],
                        title='Value'
                    ),
                    title=f'{category} Trends',
                    height=600,
                    hovermode="x unified",
                    legend=dict(
                        orientation="h",  # Horizontal legend
                        yanchor="top",   # Anchor to top of legend
                        y=-0.3,          # Position below chart (negative y moves it down)
                        xanchor="center",
                        x=0.5            # Center the legend
                    ),
                    margin=dict(b=150)   # Add bottom margin to accommodate legend
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Raw Data Section below the graph with wider display
                st.subheader("Raw Data")
                st.dataframe(
                    category_data[['Indicator Name', 'Year', 'Value']]
                    .sort_values(['Indicator Name', 'Year'])
                    .reset_index(drop=True),
                    height=400,
                    width=1000  # Set a larger width for the dataframe
                )
                
                # Show indicator list
                with st.expander("Indicator Details"):
                    st.write(f"**Available indicators ({len(available_indicators)}):**")
                    for i, ind in enumerate(available_indicators):
                        st.markdown(f"<span style='color:{colors[i]}'>■</span> {ind}", unsafe_allow_html=True)
                    
                    missing = set(indicators) - set(available_indicators)
                    if missing:
                        st.write(f"**Missing indicators ({len(missing)}):**")
                        st.write(list(missing))
            else:
                st.warning(f"No valid data available for any {category} indicators")

def show_demographic_and_population_insights(data):
    initialize_page("Demographic and Population Insights")
    st.subheader("Population Health Metrics")
    st.write("Analyze demographic trends and population health indicators.")
    
    # Show stacked area chart
    show_stacked_area_chart(data)
    
    # Show population pie charts
    show_population_piecharts(data)

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