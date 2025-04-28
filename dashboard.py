import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from categories import categories

# Background image configuration
background_images = {
    "About": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/About.jpg",
    "Overview": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Overview.jpg",
}

sidebar_image_url = "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Sidebar.png"

# Set sidebar background with an overlay
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
        color: #FFFFFF !important;  /* Change text color to white */
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

# Set main background with overlay for content readability
def set_background(image_url):
    st.markdown(f"""
    <style>
    .stApp {{
        background: url("{image_url}") no-repeat center center fixed;
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        position: relative;
        z-index: 0;
    }}

    /* Overlay for darkening the background slightly */
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        background: rgba(0, 0, 0, 0.6);  /* 60% black overlay */
        z-index: 0;
    }}

    /* Make sure all your app content appears ABOVE the overlay */
    .stApp > div {{
        position: relative;
        z-index: 1;
    }}

    /* Styling for titles and text */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
        color: #FFFFFF !important; /* White text for headings */
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3); /* Shadow for readability */
    }}

    .stMarkdown p, .stMarkdown li, .stMarkdown div {{
        color: #FFFFFF !important;  /* White text for paragraphs */
    }}

    /* Dataframe styling */
    .stDataFrame {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 8px !important;
    }}

    /* Metric card styling */
    .stMetric {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        border-radius: 8px !important;
        padding: 10px !important;
        border-left: 4px solid #FFA500 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

def initialize_page(category):
    """Initialize page without dependencies on visualizations"""
    # Set the background image for the main area and the sidebar
    image_url = background_images.get(category, None)
    if image_url:
        set_background(image_url)
    set_sidebar_background(sidebar_image_url)
    
    # Add CSS for text containers
    st.markdown("""
    <style>
    .text-container {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .metric-container {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Set title dynamically based on the category
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
    
    # Main container styling
    st.markdown("""
    <style>
    .overview-container {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #FFA500;
    }
    </style>
    """, unsafe_allow_html=True)

    # Summary section
    with st.container():
        st.markdown('<div class="overview-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Dataset Summary")
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Indicators", health_data['Indicator Name'].nunique())
            st.metric("Years Covered", f"{health_data['Year'].min()} to {health_data['Year'].max()}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.subheader("Value Statistics")
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            health_data['Value'] = pd.to_numeric(health_data['Value'], errors='coerce')
            st.metric("Average Value", f"{health_data['Value'].mean():.2f}")
            st.metric("Data Points", len(health_data.dropna(subset=['Value'])))
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Category trends with improved containers
    st.subheader("Category Trends Animation")
    tabs = st.tabs(list(categories.keys()))
    
    for tab, (category, indicators) in zip(tabs, categories.items()):
        with tab:
            with st.container():
                st.markdown('<div class="overview-container">', unsafe_allow_html=True)
                
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
    
    st.markdown("""
    <style>
    .insights-container {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="insights-container">', unsafe_allow_html=True)

        demographic_indicators = categories.get("Population Health and Demographics", [])
        
        # Filter data for demographics
        demo_data = data[
            (data['Indicator Name'].isin(demographic_indicators)) & 
            (data['Value'].notna())
        ].copy()

        if not demo_data.empty:
            st.write(f"Found {demo_data['Indicator Name'].nunique()} demographic indicators.")
            
            # Stacked Area Chart
            fig = px.area(
                demo_data,
                x='Year',
                y='Value',
                color='Indicator Name',
                labels={'Value': 'Indicator Value', 'Year': 'Year'},
                title="Demographic Trends Over Time",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig.update_layout(
                height=600,
                hovermode="x unified",
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                ),
                margin=dict(b=150)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Raw data section
            st.subheader("Demographic Data Table")
            st.dataframe(
                demo_data[['Indicator Name', 'Year', 'Value']].sort_values(['Indicator Name', 'Year']).reset_index(drop=True),
                height=400,
                width=1000
            )

            # Indicator details
            with st.expander("Indicator Details"):
                for indicator in sorted(demographic_indicators):
                    st.markdown(f"• {indicator}")

        else:
            st.warning("No demographic indicators with available data.")

        st.markdown('</div>', unsafe_allow_html=True)

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


def show_key_indicator_highlights(data):
    initialize_page("Key Indicator Highlights")
    
    st.markdown("""
    ## Key Indicator Highlights
    Track the most important health indicators over time.
    """)
    
    # Define key indicators (you can customize this list)
    key_indicators = [
        "Life expectancy at birth, total (years)",
        "Mortality rate, infant (per 1,000 live births)",
        "Current health expenditure (% of GDP)",
        "Prevalence of undernourishment (% of population)",
        "Immunization, measles (% of children ages 12-23 months)"
    ]
    
    # Filter to only include available indicators
    available_indicators = [ind for ind in key_indicators if ind in data['Indicator Name'].unique()]
    
    if not available_indicators:
        st.warning("No key indicator data available")
        return
    
    # Show metrics for latest year
    st.subheader("Latest Values")
    latest_year = data['Year'].max()
    latest_data = data[data['Year'] == latest_year]
    
    cols = st.columns(3)
    for idx, indicator in enumerate(available_indicators):
        value = latest_data[latest_data['Indicator Name'] == indicator]['Value'].values
        if len(value) > 0:
            cols[idx % 3].metric(
                label=indicator,
                value=format_value(value[0]),
                help=f"Year: {latest_year}"
            )
    
    # Show trend charts
    st.subheader("Historical Trends")
    for indicator in available_indicators:
        indicator_data = data[data['Indicator Name'] == indicator]
        if not indicator_data.empty:
            fig = px.line(
                indicator_data,
                x='Year',
                y='Value',
                title=indicator,
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)

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
def show_dashboard(data):
    st.markdown("---")