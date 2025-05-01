# Sri Lanka Health Dashboard

An interactive dashboard visualizing key health indicators for Sri Lanka (1960-2023) with animated trends, comparative analysis, and geographic context.

https://srilankahealthdashboard.streamlit.app/

## Features

### Animated Visualizations
- **12 category-specific animated charts** showing health trends over six decades
- **Indicator code reference** for easy interpretation
- **Multiple chart types** including:
  - Line charts with markers
  - Area charts
  - Bar charts
  - Heatmaps
  - Scatter plots
  - Box plots

### Dashboard Pages
1. **Overview**
   - Key statistics and metrics
   - Data coverage analysis
   - Category distribution
   - Performance trends

2. **Category-Specific Analysis** (12 categories)
   - Mortality Rates
   - Maternal and Child Health
   - Infectious Diseases
   - Health Expenditure
   - Healthcare Infrastructure
   - Water/Sanitation/Hygiene
   - Non-communicable Diseases
   - Nutrition/Food Security
   - Demographic Indicators
   - Reproductive Health
   - Civil Registration
   - Injury/External Causes

3. **Comparative Insights**
   - Multi-indicator comparison
   - Correlation analysis
   - Statistical summaries

4. **About Section**
   - Project information
   - Interactive map of Sri Lanka
   - Key geographic features

### Interactive Features
- **Temporal Filtering**:
  - Custom year range selection (1960-2023)

- **Data Selection**:
  - Multi-indicator comparison
  - Category filtering
  - Keyword-based filtering

- **Visual Customization**:
  - Chart type selection
  - Color schemes
  - Legend positioning

- **Geospatial Context**:
  - Interactive Folium map
  - Key city markers
  - Geographic highlights

## Technical Details

### Built With
- **Python** (3.9+)
- **Streamlit** - Web framework
- **Plotly** - Interactive visualizations
- **Folium** - Interactive maps
- **Pandas** - Data manipulation
- **Statsmodels** - Statistical analysis

### Dependencies
See [requirements.txt](requirements.txt) for complete list

### Deployment
Deployed on Streamlit Community Cloud:
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_STREAMLIT_URL)

## Data Sources
- World Bank Health Indicators
- Sri Lanka Health Ministry Reports
- WHO Global Health Observatory

## How to Use
1. Select a category from the sidebar
2. Adjust filters as needed
3. Interact with visualizations
4. Use animation controls for time-series data
5. Compare multiple indicators in Comparative Insights
