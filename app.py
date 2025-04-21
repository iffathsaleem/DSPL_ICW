import streamlit as st
import pandas as pd
import plotly.express as px

health = pd.read_csv("Sri Lanka Health Statistics.csv")

st.title("Sri Lankan Health Indicators Dashboard")