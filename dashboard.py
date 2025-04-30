import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from categories import categories
from sidebar import SECTION_BACKGROUNDS, set_section_background

# Background image configuration
background_images = {
    "About": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/About.jpg",
    "Overview": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Overview.jpg",
    **SECTION_BACKGROUNDS  # Merge with section-specific backgrounds
}

def initialize_page(category):
    """Initialize page with proper background and styling"""
    set_section_background(category)
    st.title(f"{category}")

def format_value(value, is_percentage=False):
    """Format numbers consistently"""
    if pd.isna(value):
        return "N/A"
    if is_percentage:
        return f"{value:.2f}%"
    if isinstance(value, (int, float)) and float(value).is_integer():
        return f"{int(value):,}"
    return f"{value:,.2f}"

def show_overview(health_data):
    # Set background with proper styling
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                   url('{background_images["Overview"]}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .metric-card {{
        background-color: rgba(30, 30, 30, 0.8);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}
    </style>
    """, unsafe_allow_html=True)
    
    st.title("Sri Lanka Health Dashboard Overview")
    st.markdown("---")
    
    # Key Metrics Section
    st.header("Key Discoveries")
    
    # Data completeness analysis
    latest_year = health_data['Year'].max()
    year_range = f"{health_data['Year'].min()} to {health_data['Year'].max()}"
    coverage_pct = len(health_data[health_data['Year'] == latest_year]) / len(health_data) * 100
    
    cols = st.columns(3)
    with cols[0]:
        st.metric("Total Indicators", health_data['Indicator Name'].nunique())
    with cols[1]:
        st.metric("Years Covered", year_range)
    with cols[2]:
        st.metric(f"{latest_year} Data Coverage", f"{coverage_pct:.1f}%")
    
    # Category Distribution
    st.subheader("Data Composition")
    category_counts = health_data.groupby('Category').size().reset_index(name='Count')
    fig = px.pie(category_counts, names='Category', values='Count', 
                 hole=0.3, color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance Highlights
    st.markdown("---")
    st.header("Performance Trends")
    
    # Calculate 10-year change for available metrics
    health_data['Value'] = pd.to_numeric(health_data['Value'], errors='coerce')
    current_avg = health_data[health_data['Year'] == latest_year]['Value'].mean()
    past_avg = health_data[health_data['Year'] == latest_year-10]['Value'].mean()
    avg_change = ((current_avg - past_avg) / past_avg * 100) if past_avg != 0 else 0
    
    cols = st.columns(3)
    with cols[0]:
        st.metric("Average Value", f"{current_avg:.1f}", 
                 f"{avg_change:.1f}% vs 10y ago")
    with cols[1]:
        complete_series = health_data.groupby('Indicator Name')['Year'].nunique().max()
        st.metric("Most Complete Series", f"{complete_series} years")
    
    # Original Animated Category Trends (preserved exactly as in original code)
    st.markdown("---")
    st.header("Animated Category Trends (1960-2023)")
    tabs = st.tabs(list(categories.keys()))
    
    for tab, (category, indicators) in zip(tabs, categories.items()):
        with tab:
            category_data = health_data[
                (health_data['Indicator Name'].isin(indicators)) &
                (health_data['Value'].notna())
            ].copy()
            
            # Filter years to 1960-2023
            category_data = category_data[(category_data['Year'] >= 1960) & (category_data['Year'] <= 2023)]
            
            if not category_data.empty:
                # Get unique indicator names and codes
                available_indicators = category_data[['Indicator Name', 'Indicator_Code']].drop_duplicates()
                st.write(f"Showing {len(available_indicators)} of {len(indicators)} indicators for {category}")
                
                # Create figure with proper spacing
                fig = go.Figure()
                
                # Add traces using Indicator_Code in legend
                colors = px.colors.qualitative.Plotly
                for i, row in available_indicators.iterrows():
                    indicator_name = row['Indicator Name']
                    indicator_code = row['Indicator_Code']
                    indicator_data = category_data[category_data['Indicator Name'] == indicator_name]
                    
                    fig.add_trace(go.Scatter(
                        x=indicator_data['Year'],
                        y=indicator_data['Value'],
                        name=indicator_code,
                        mode='lines+markers',
                        marker=dict(size=10),
                        line=dict(width=4),
                        marker_color=colors[i % len(colors)],
                        hovertemplate=f"{indicator_name}<br>Year: %{{x}}<br>Value: %{{y}}<extra></extra>",
                        customdata=[indicator_name] * len(indicator_data)
                    ))
                
                # Set up layout with increased spacing
                fig.update_layout(
                    height=1100,
                    width=1200,
                    template='plotly_dark',
                    margin=dict(l=100, r=100, t=100, b=350),
                    
                    # X-axis configuration
                    xaxis=dict(
                        title='Year',
                        showline=True,
                        showgrid=False,
                        range=[1960, 2023],
                        tickmode='linear',
                        tick0=1960,
                        dtick=10,
                        tickfont=dict(size=14),
                        title_font=dict(size=16),
                        ticklen=10,
                        tickwidth=2,
                        ticks='outside'
                    ),
                    
                    # Y-axis configuration
                    yaxis=dict(
                        title='Value',
                        showgrid=True,
                        gridcolor='rgba(100, 100, 100, 0.3)',
                        tickfont=dict(size=14),
                        title_font=dict(size=16)
                    ),
                    
                    # Legend positioned higher with more space below
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=-0.35,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=12),
                        itemwidth=40,
                        bgcolor='rgba(0,0,0,0.5)'
                    ),
                    
                    # Buttons moved down
                    updatemenus=[dict(
                        type="buttons",
                        showactive=True,
                        buttons=[
                            dict(label="PLAY", method="animate", args=[None]),
                            dict(label="PAUSE", method="animate", args=[[None], {"frame": {"duration": 0}}])
                        ],
                        x=0.1,
                        xanchor="right",
                        y=-0.5,
                        yanchor="top",
                        pad=dict(t=20, b=20),
                        bgcolor='rgba(0,0,0,0.7)'
                    )],
                    
                    # Slider with adjusted spacing
                    sliders=[dict(
                        currentvalue={"prefix": "YEAR: ", "font": {"size": 14}},
                        pad=dict(t=120, b=50),
                        steps=[dict(args=[[str(year)], dict(mode="immediate")], 
                              label=str(year), 
                              method="animate") 
                        for year in range(1960, 2024)]
                    )]
                )
                
                # Create animation frames
                frames = []
                for year in range(1960, 2024):
                    frames.append(go.Frame(
                        data=[go.Scatter(
                            x=category_data[(category_data['Year'] <= year) & 
                                          (category_data['Indicator Name'] == row['Indicator Name'])]['Year'],
                            y=category_data[(category_data['Year'] <= year) & 
                                          (category_data['Indicator Name'] == row['Indicator Name'])]['Value'],
                        ) for _, row in available_indicators.iterrows()],
                        name=str(year)
                    ))
                
                fig.frames = frames
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Add gap before reference table
                st.markdown("<div style='margin-top:100px;'></div>", unsafe_allow_html=True)
                
                # Create collapsible indicator code mapping table
                with st.expander("Indicator Code Reference", expanded=False):
                    mapping_table = available_indicators[['Indicator_Code', 'Indicator Name']] \
                        .rename(columns={'Indicator_Code': 'Indicator Code'}) \
                        .sort_values('Indicator Code') \
                        .reset_index(drop=True)
                    
                    st.dataframe(
                        mapping_table.style.apply(
                            lambda x: ['background: #222222' if i%2==0 else 'background: #444444' 
                                     for i in range(len(x))],
                            axis=1
                        ),
                        use_container_width=True,
                        height=min(400, 35 * len(mapping_table) + 38)
                    )
                
                st.subheader("Raw Data")
                st.dataframe(
                    category_data[['Indicator_Code', 'Indicator Name', 'Year', 'Value']]
                    .rename(columns={'Indicator_Code': 'Indicator Code'})
                    .sort_values(['Indicator Code', 'Year'])
                    .reset_index(drop=True),
                    use_container_width=True
                )
            else:
                st.warning(f"No data available for {category} indicators")

def show_category_analysis(data, category_name):
    """Unified category analysis function with fixed legend positioning"""
    initialize_page(category_name)
    
    indicators = categories.get(category_name.replace(" Analysis", ""), [])
    if not indicators:
        st.warning("No indicators defined for this category")
        return
    
    data['Value'] = pd.to_numeric(data['Value'], errors='coerce')
    category_data = data[data['Indicator Name'].isin(indicators)].dropna(subset=['Value'])
    
    if not category_data.empty:
        # Comparative line chart with optimized layout
        st.subheader(f"{category_name} Trends")
        fig = px.line(
            category_data,
            x='Year',
            y='Value',
            color='Indicator Name',
            markers=True,
            template='plotly_dark',
            height=650  # Slightly reduced to accommodate legend
        )
        
        # Enhanced legend and layout with dynamic positioning
        num_indicators = len(category_data['Indicator Name'].unique())
        
        # Calculate dynamic margin based on number of indicators
        bottom_margin = max(150, num_indicators * 7)  # At least 150px, more if many indicators
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0.5)',
            paper_bgcolor='rgba(0,0,0,0.3)',
            legend=dict(
                orientation="h",
                yanchor="top",  # Anchor to top of legend
                y=-0.3 - (0.02 * num_indicators),  # Dynamic vertical position
                xanchor="center",
                x=0.5,
                font=dict(size=10),  # Slightly smaller font
                itemwidth=30,  # More compact items
                itemsizing='constant'  # Consistent icon sizes
            ),
            margin=dict(
                b=bottom_margin,  # Dynamic bottom margin
                t=50,
                l=50,
                r=50
            ),
            hovermode="x unified",
            autosize=True
        )
        
        # Add some space after the chart
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("<div style='margin-bottom:50px'></div>", unsafe_allow_html=True)
        
        # Rest of the function remains the same...
        # Latest values metrics
        st.subheader("Latest Values")
        latest_year = category_data['Year'].max()
        latest_data = category_data[category_data['Year'] == latest_year]
        
        cols = st.columns(3)
        for idx, (_, row) in enumerate(latest_data.iterrows()):
            with cols[idx % 3]:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <h4>{row['Indicator Name']}</h4>
                        <p style="font-size: 24px; font-weight: bold;">
                            {format_value(row['Value'])}
                        </p>
                        <p>Year: {latest_year}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        # Detailed data table
        st.subheader("Detailed Data")
        st.dataframe(
            category_data[['Indicator Name', 'Year', 'Value']]
            .sort_values(['Indicator Name', 'Year'])
            .reset_index(drop=True),
            use_container_width=True,
            height=500
        )
    else:
        st.warning("No valid data available for selected indicators")

        
# Category-specific functions
def show_demographic_insights(data):
    show_category_analysis(data, "Demographic Indicators Analysis")

def show_health_expenditure_insights(data):
    show_category_analysis(data, "Health Expenditure Analysis")

def show_mortality_trends(data):
    show_category_analysis(data, "Mortality Rates Analysis")

def show_maternal_child_health(data):
    show_category_analysis(data, "Maternal and Child Health Analysis")

def show_infectious_diseases(data):
    show_category_analysis(data, "Infectious Diseases Analysis")

def show_healthcare_infrastructure(data):
    show_category_analysis(data, "Healthcare Infrastructure and Services Analysis")

def show_water_sanitation(data):
    show_category_analysis(data, "Water, Sanitation and Hygiene Analysis")

def show_non_communicable_diseases(data):
    show_category_analysis(data, "Non-communicable Diseases and Risk Factors Analysis")

def show_nutrition(data):
    show_category_analysis(data, "Nutrition and Food Security Analysis")

def show_reproductive_health(data):
    show_category_analysis(data, "Reproductive Health Analysis")

def show_civil_registration(data):
    show_category_analysis(data, "Civil Registration Analysis")

def show_injury_causes(data):
    show_category_analysis(data, "Injury and External Causes Analysis")

def show_dashboard(data):
    st.markdown("---")