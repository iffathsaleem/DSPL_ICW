import streamlit as st
import pandas as pd
import plotly.express as px

health = pd.read_csv("Sri Lanka Health Statistics.csv")

# Clean column names
health.columns = health.columns.str.strip()
health["Year"] = health["Year"].astype(int)

# Sidebar: Indicator selection
indicators = st.sidebar.multiselect(
    "Select Health Indicators",
    health["Indicator Name"].unique(),
    default=["Total alcohol consumption per capita, female (liters of pure alcohol, projected estimates, female 15+ years of age)"]
)

# Sidebar: Year selection
year_selection_mode = st.sidebar.radio("Select Year Mode", ["Single Year", "Year Range"])

if year_selection_mode == "Single Year":
    year = st.sidebar.selectbox("Select Year", sorted(health["Year"].unique()))
    selected_years = (year, year)
else:
    selected_years = st.sidebar.slider(
        "Select Year Range",
        min_value=int(health["Year"].min()),
        max_value=int(health["Year"].max()),
        value=(1960, 2023)
    )

# Sidebar: Sorting option for year
sort_order = st.sidebar.radio("Sort Year", ["Oldest to Newest", "Newest to Oldest"])


filtered = health[
    (health["Indicator Name"].isin(indicators)) &
    (health["Year"].between(selected_years[0], selected_years[1]))
]


if sort_order == "Newest to Oldest":
    filtered = filtered.sort_values(by="Year", ascending=False)
else:
    filtered = filtered.sort_values(by="Year", ascending=True)

# Main page
if filtered.empty:
    st.warning("No data available for the selected filters.")
else:
    st.subheader("Filtered Health Data")
    st.dataframe(filtered)  

# Making Chart Using Filtered Data
if filtered.empty:
    st.warning("No data available for the selected filters.")
else:
    # Plot the data
    fig = px.line(
    filtered,
    x="Year", 
    y="Value", 
    color="Indicator Name", 
    markers=True,
    title="Health Indicator Trends in Sri Lanka",
    height=500
)

# Chart Legend
fig.update_layout(
    legend=dict(
        orientation="h",        
        yanchor="bottom",       
        y=-0.5,               
        xanchor="center",       
        x=0.5
    ),
    margin=dict(
        b=150                   
    )
)


st.plotly_chart(fig, use_container_width=True)