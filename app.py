import streamlit as st
import pandas as pd
import plotly.express as px 
from about import show_about
from sidebar import sidebar_filters

health = pd.read_csv("Sri Lanka Health Statistics.csv")

# Clean column names
health.columns = health.columns.str.strip()
health["Year"] = health["Year"].astype(int)

# Sidebar logic
view, category, selected_indicators, year_range, sort_order = sidebar_filters(health)

# About Section
if view == "About":
    show_about()
# Indicator Charts
elif selected_indicators:
    filtered = health[health["Indicator Name"].isin(selected_indicators)]
    filtered = filtered[(filtered["Year"] >= year_range[0]) & (filtered["Year"] <= year_range[1])]
    filtered = filtered.sort_values(by="Year", ascending=(sort_order == "Oldest to Newest"))

    if not filtered.empty:
        fig = px.line(filtered, x="Year", y="Value", color="Indicator Name", markers=True,
                      title=f"{category} Trends in Sri Lanka")
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="center", x=0.5))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")
