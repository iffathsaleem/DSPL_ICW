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
    initialize_page("Overview")
    
    # Summary section
    with st.container():
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

    # Animated bubble chart showing trends across all categories
    st.subheader("Animated Trends Across Categories")
    
    # Prepare data for animation
    animation_data = health_data.copy()
    animation_data['Year'] = animation_data['Year'].astype(str)  # For proper animation
    
    # Create a mapping of indicators to categories
    indicator_to_category = {}
    for category, indicators in categories.items():
        for indicator in indicators:
            indicator_to_category[indicator] = category
    
    # Add category column to data
    animation_data['Category'] = animation_data['Indicator Name'].map(indicator_to_category)
    
    # Create animated bubble chart
    try:
        fig = px.scatter(
            animation_data.dropna(subset=['Value', 'Category']),
            x="Year",
            y="Value",
            animation_frame="Year",
            size="Value",
            color="Category",
            hover_name="Indicator Name",
            size_max=60,
            range_y=[0, animation_data['Value'].max() * 1.1],
            height=700,
            template='plotly_dark',
            title="Health Indicators Trend Animation"
        )
        
        # Improve animation settings
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
        fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 500
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Could not create animated chart: {str(e)}")
        st.write("Showing static visualization instead")
        
        # Fallback to static visualization
        fig = px.scatter(
            animation_data.dropna(subset=['Value', 'Category']),
            x="Year",
            y="Value",
            color="Category",
            hover_name="Indicator Name",
            size="Value",
            size_max=60,
            height=700,
            template='plotly_dark'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Category trends (your existing code)
    st.subheader("Category Trends")
    tabs = st.tabs(list(categories.keys()))
    
    for tab, (category, indicators) in zip(tabs, categories.items()):
        with tab:
            category_data = health_data[
                (health_data['Indicator Name'].isin(indicators)) &
                (health_data['Value'].notna())
            ].copy()
            
            if not category_data.empty:
                available_indicators = category_data['Indicator Name'].unique()
                st.write(f"Showing {len(available_indicators)} of {len(indicators)} indicators for {category}")
                
                # Create figure with larger size
                fig = go.Figure()
                colors = px.colors.qualitative.Plotly
                
                for i, indicator in enumerate(available_indicators):
                    indicator_data = category_data[category_data['Indicator Name'] == indicator]
                    color = colors[i % len(colors)]
                    fig.add_trace(go.Scatter(
                        x=indicator_data['Year'],
                        y=indicator_data['Value'],
                        name=indicator,
                        mode='lines+markers',
                        marker=dict(size=8),
                        line=dict(width=3),
                        marker_color=color,
                        line_color=color
                    ))
                
                fig.update_layout(
                    height=700,
                    width=1000,
                    template='plotly_dark',
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.5,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=12),
                        itemwidth=40
                    ),
                    margin=dict(b=200)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("Raw Data")
                st.dataframe(
                    category_data[['Indicator Name', 'Year', 'Value']]
                    .sort_values(['Indicator Name', 'Year'])
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