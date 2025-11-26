import streamlit as st
import pandas as pd
import altair as alt
from Utils import queries
from Utils import charts
from Utils import config_page

config_page.config()


months = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}


months_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

national_data = queries.get_precovid_totals()

national_data["Unemployment Rate"] = national_data["Unemployment"] / national_data["Labor Force"]
national_data["Unemployment Rate Change"] = national_data["Unemployment Rate"].shift(1)
national_data["Unemployment Rate Change"] = national_data["Unemployment Rate Change"] - national_data["Unemployment Rate"]

national_data["Date"] = pd.to_datetime(national_data["Date"])
national_data["Month"] = national_data["Date"].dt.month_name()
average_year = national_data.groupby("Month")["Unemployment Rate Change"].mean().reset_index()

average_year["Month"] = pd.Categorical(average_year["Month"], categories=months_order, ordered=True)

state_data = queries.get_precovid_data()
state_data = state_data.sort_values(["State/Area", "Date"])

state_data["Unemployment Rate Change"] = state_data.groupby("State/Area")["Unemployment Rate"].shift(1)
state_data["Unemployment Rate Change"] = state_data["Unemployment Rate Change"] - state_data["Unemployment Rate"]


average_month_country = (
    state_data.groupby(["State/Area", "Month"])["Unemployment Rate Change"]
    .mean()
    .reset_index()
    .sort_values(["State/Area", "Month"])
)


average_month_country["Month"] = average_month_country["Month"].map(months)

average_year["State/Area"] = "Total"
average_year = pd.concat([average_month_country , average_year])


states = st.multiselect("Choose states", list(average_year["State/Area"].unique()), ["Total","Iowa"])

if not states:
    st.error("Choose a state.")
else:
    average_year = average_year.set_index("State/Area")
    data = average_year.loc[states]
    data = data.reset_index()

    charts.bar_multi_chart(data, "Month", "Unemployment Rate Change", "State/Area:N", months_order, "%")
    charts.point_multi_chart(data, "Month", "Unemployment Rate Change", "State/Area:N", months_order, "%")

