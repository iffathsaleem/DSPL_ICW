import streamlit as st
import pandas as pd
import plotly.express as px

def show_dashboard(df, category, selected_indicators, year_range, sort_order, keyword_filter):
    st.title("Health Data Dashboard")
    start_year, end_year = year_range
    filtered = df[df['Year'].between(start_year, end_year)]

    # Sort data
    ascending = True if sort_order == "Oldest to Newest" else False
    filtered = filtered.sort_values("Year", ascending=ascending)

    if selected_indicators:
        # Pie Chart: Total contributions
        st.subheader(f"Indicator Contribution in {category}")
        pie_data = filtered[filtered["Indicator Name"].isin(selected_indicators)]
        pie_summary = pie_data.groupby("Indicator Name")["Value"].sum().reset_index()
        fig_pie = px.pie(pie_summary, names="Indicator Name", values="Value", title="Percentage Contribution")
        st.plotly_chart(fig_pie)

        # Line chart + data table for each indicator
        for indicator in selected_indicators:
            st.subheader(f"{indicator} Over Time")

            chart_data = filtered[filtered["Indicator Name"] == indicator]

            fig_line = px.line(chart_data, x="Year", y="Value", color="Country Name", title=indicator)
            st.plotly_chart(fig_line)

            st.dataframe(chart_data[["Country Name", "Year", "Value"]])
    else:
        st.info("Please select at least one indicator to view visualizations and data.")
