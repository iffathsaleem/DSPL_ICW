import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from categories import categories
from sidebar import SECTION_BACKGROUNDS, set_section_background

background_images = {
    "About": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/About.jpg",
    "Overview": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Overview.jpg",
    "Comparative Insights": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Trends%20Overtime.JPG",
    "Executive Summary": "https://raw.githubusercontent.com/iffathsaleem/DSPL_ICW/main/Images/Key%20Indicator%20Highlights.jpg",
    **SECTION_BACKGROUNDS
}

def apply_custom_styling():
    st.markdown("""
    <style>
        .metric-card {
            background-color: rgba(30, 30, 30, 0.8);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.4);
        }
        .metric-card h4 {
            color: #e0e0e0;
            font-size: 16px;
            margin-bottom: 10px;
            font-weight: 500;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 8px;
        }
        .indicator-value {
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            margin: 10px 0;
        }
        .year-label {
            font-size: 14px;
            color: #aaaaaa;
            font-style: italic;
        }
        .section-divider {
            margin: 40px 0;
            border-top: 1px solid rgba(255,255,255,0.1);
        }
        .section-header {
            background-color: rgba(0,0,0,0.4);
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #2986cc;
        }
    </style>
    """, unsafe_allow_html=True)

def initialize_page(category):
    set_section_background(category)
    st.markdown(f"<h1 class='section-header'>{category}</h1>", unsafe_allow_html=True)

def format_value(value, is_percentage=False):
    if pd.isna(value):
        return "N/A"
    if is_percentage or (isinstance(value, (int, float)) and 0 <= value <= 100):
        return f"{value:.2f}%"
    if isinstance(value, (int, float)) and float(value).is_integer():
        return f"{int(value):,}"
    return f"{value:,.2f}"

def show_overview(health_data):
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('{background_images["Overview"]}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    st.title("Sri Lanka Health Dashboard Overview")
    
    st.markdown("""
    ## Period-Specific Insights
    
    #### Post-War Recovery (2009-2015)
    - Rapid improvements in maternal and child health indicators
    - Increased health expenditure as % of GDP
    
    #### Economic Challenges (2016-2022)
    - Pressure on health financing metrics
    - Resilient performance in key outcome indicators
    
    #### COVID-19 Impact (2020-2022)
    - Disruptions in routine health services
    - Shifts in mortality patterns
    """)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
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
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.subheader("Data Composition")
    
    category_counts = health_data.groupby('Category').size().reset_index(name='Count')
    fig = px.pie(
        category_counts, 
        names='Category', 
        values='Count', 
        hole=0.3, 
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0.3)',
        paper_bgcolor='rgba(0,0,0,0.3)',
        margin=dict(t=40, b=40, l=20, r=20),
        font=dict(color='white'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=11)
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.header("Performance Trends")
    
    health_data['Value'] = pd.to_numeric(health_data['Value'], errors='coerce')
    current_avg = health_data[health_data['Year'] == latest_year]['Value'].mean()
    past_avg = health_data[health_data['Year'] == latest_year-10]['Value'].mean()
    avg_change = ((current_avg - past_avg) / past_avg * 100) if past_avg != 0 else 0
    
    cols = st.columns(3)
    with cols[0]:
        st.metric("Average Value", f"{current_avg:.1f}", f"{avg_change:.1f}% vs 10y ago")
    with cols[1]:
        complete_series = health_data.groupby('Indicator Name')['Year'].nunique().max()
        st.metric("Most Complete Series", f"{complete_series} years")
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.header("Animated Category Trends (1960-2023)")
    tabs = st.tabs(list(categories.keys()))
    
    for tab, (category, indicators) in zip(tabs, categories.items()):
        with tab:
            category_data = health_data[
                (health_data['Indicator Name'].isin(indicators)) &
                (health_data['Value'].notna())
            ].copy()
            
            category_data = category_data[(category_data['Year'] >= 1960) & (category_data['Year'] <= 2023)]
            
            if not category_data.empty:
                available_indicators = category_data[['Indicator Name', 'Indicator_Code']].drop_duplicates()
                st.write(f"Showing {len(available_indicators)} of {len(indicators)} indicators for {category}")
                
                fig = go.Figure()
                
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
                
                fig.update_layout(
                    height=1100,
                    width=1200,
                    template='plotly_dark',
                    margin=dict(l=100, r=100, t=100, b=350),
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
                    yaxis=dict(
                        title='Value',
                        showgrid=True,
                        gridcolor='rgba(100, 100, 100, 0.3)',
                        tickfont=dict(size=14),
                        title_font=dict(size=16)
                    ),
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
                    sliders=[dict(
                        currentvalue={"prefix": "YEAR: ", "font": {"size": 14}},
                        pad=dict(t=120, b=50),
                        steps=[
                            dict(
                                args=[[str(year)], dict(mode="immediate")], 
                                label=str(year), 
                                method="animate"
                            ) 
                            for year in range(1960, 2024)
                        ]
                    )]
                )
                
                frames = []
                for year in range(1960, 2024):
                    frame_data = []
                    for _, row in available_indicators.iterrows():
                        year_data = category_data[
                            (category_data['Year'] <= year) & 
                            (category_data['Indicator Name'] == row['Indicator Name'])
                        ]
                        frame_data.append(
                            go.Scatter(
                                x=year_data['Year'],
                                y=year_data['Value']
                            )
                        )
                    frames.append(go.Frame(data=frame_data, name=str(year)))

                fig.frames = frames
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("<div style='margin-top:100px;'></div>", unsafe_allow_html=True)
                
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

def show_category_analysis(data, category_name):
    apply_custom_styling()
    initialize_page(category_name)
    
    if data.empty:
        st.warning(f"No data available for {category_name}")
        return
    
    if not pd.api.types.is_numeric_dtype(data['Value']):
        data['Value'] = pd.to_numeric(data['Value'], errors='coerce')

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.subheader("Basic Statistics")
    cols = st.columns(3)
    with cols[0]:
        st.metric("Indicators Available", len(data['Indicator Name'].unique()))
    with cols[1]:
        st.metric("Years Covered", f"{int(data['Year'].min())} - {int(data['Year'].max())}")
    with cols[2]:
        latest_year = data['Year'].max()
        latest_coverage = len(data[data['Year'] == latest_year]) / len(data) * 100
        st.metric(f"{latest_year} Coverage", f"{latest_coverage:.1f}%")
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.subheader("Trend Analysis")
    fig = px.line(
        data,
        x='Year',
        y='Value',
        color='Indicator Name',
        markers=True,
        template='plotly_dark',
        height=600
    )
    
    num_indicators = len(data['Indicator Name'].unique())
    legend_height = max(150, num_indicators * 7)
    
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.3 - (0.02 * num_indicators),
            xanchor="center",
            x=0.5,
            font=dict(size=10),
            itemwidth=30
        ),
        margin=dict(b=legend_height),
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.subheader("Yearly Distribution")
    
    all_years = sorted(data['Year'].unique())
    default_selection = all_years[:5] + all_years[-5:]
    
    st.write("Select years to display:")
    cols = st.columns(3)
    selected_years = []
    
    for i, year in enumerate(all_years):
        with cols[i % 3]:
            if st.checkbox(str(year), value=(year in default_selection), key=f"year_{year}"):
                selected_years.append(year)
    
    if not selected_years:
        st.warning("Please select at least one year")
    else:
        filtered_data = data[data['Year'].isin(selected_years)]
        indicator_map = data[['Indicator Name', 'Indicator_Code']].drop_duplicates()
        indicator_map = dict(zip(indicator_map['Indicator Name'], indicator_map['Indicator_Code']))
        
        for year in selected_years:
            st.markdown(f"### {year} Distribution")
            year_data = filtered_data[filtered_data['Year'] == year]
            if not year_data.empty:
                fig = px.pie(
                    year_data,
                    names='Indicator_Code',
                    values='Value',
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    custom_data=['Indicator Name']
                )
                
                fig.update_traces(
                    hovertemplate="<b>%{label}</b><br>%{customdata[0]}<br>Value: %{value}<br>Percentage: %{percent}",
                    textposition='inside',
                    textinfo='percent+label',
                    textfont_size=12
                )
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0.3)',
                    paper_bgcolor='rgba(0,0,0,0.3)',
                    margin=dict(t=40, b=40, l=20, r=20),
                    font=dict(color='white'),
                    legend=dict(
                        orientation="v",
                        yanchor="middle",
                        y=0.5,
                        xanchor="right",
                        x=1.3,
                        font=dict(size=10),
                        title_text='Indicator Codes'
                    ),
                    uniformtext_minsize=10,
                    uniformtext_mode='hide'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown(f"**Indicator Reference for {year}**")
                ref_df = year_data[['Indicator_Code', 'Indicator Name', 'Value']]
                ref_df = ref_df.rename(columns={
                    'Indicator_Code': 'Code',
                    'Indicator Name': 'Name',
                    'Value': 'Value'
                }).sort_values('Code')
                
                st.dataframe(
                    ref_df.style.format({'Value': '{:,.2f}'}),
                    use_container_width=True,
                    height=min(300, 35 * len(ref_df) + 38)
                )
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.subheader("Latest Values")
    latest_year = data['Year'].max()
    latest_data = data[data['Year'] == latest_year]
    
    if not latest_data.empty:
        cols = st.columns(3)
        for idx, (_, row) in enumerate(latest_data.iterrows()):
            with cols[idx % 3]:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <h4>{row['Indicator Name']}</h4>
                        <p class="indicator-value">{format_value(row['Value'])}</p>
                        <p class="year-label">Year: {latest_year}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.subheader("Detailed Data")
    st.dataframe(
        data[['Indicator_Code', 'Indicator Name', 'Year', 'Value', 'Category']]
        .sort_values(['Indicator Name', 'Year'])
        .reset_index(drop=True),
        use_container_width=True,
        height=500
    )

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
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                   url('{background_images.get("Comparative Insights", "")}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)
    st.markdown("---")