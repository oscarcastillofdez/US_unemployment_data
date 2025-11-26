import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from Utils import queries
from Utils import charts
from Utils import config_page

config_page.config()

complete_data = queries.get_complete_data()


state = st.selectbox("Select a state", list(complete_data["State/Area"].unique()))

state_data = complete_data.set_index("State/Area")
state_data = state_data.loc[state]

charts.red_area_chart(state_data, "Date", "Unemployment Rate", y_format="%")

last_unemployment_rate = state_data.iloc[-1]["Unemployment Rate"] * 100
mean_unemployment_rate = state_data["Unemployment Rate"].mean() * 100
last_employment_rate = state_data.iloc[-1]["Employment Rate"] * 100
mean_employment_rate = state_data["Employment Rate"].mean() * 100
last_lfr_rate = state_data.iloc[-1]["Labor Force Rate"] * 100
mean_lfr_rate = state_data["Labor Force Rate"].mean() * 100

col1, col2, col3 = st.columns([1,1,1])

with col1:
    charts.gauge_chart(last_unemployment_rate, 0, 100, mean_unemployment_rate)
with col2:
    charts.gauge_chart(last_employment_rate, 0, 100, mean_employment_rate)
with col3:
    charts.gauge_chart(last_lfr_rate, 0, 100, mean_lfr_rate)

