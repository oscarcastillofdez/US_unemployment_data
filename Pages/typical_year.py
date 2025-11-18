import streamlit as st
import pandas as pd
import altair as alt
from Utils import queries
from Utils import charts
from Utils import config_page

config_page.config()

df = queries.get_average_change_year()

meses = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

months = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}

orden_meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

months_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

df["mes_nombre"] = df["Month"].map(meses)



df["mes_nombre"] = pd.Categorical(df["mes_nombre"], categories=orden_meses, ordered=True)

df.set_index("mes_nombre")

charts.good_line_chart(df, "mes_nombre", "Non-Institutional Population Change")
charts.good_line_chart(df, "mes_nombre", "Labor Force Change")
charts.good_line_chart(df, "mes_nombre", "Employment Change")
charts.good_bar_chart(df, "mes_nombre", "Unemployment Change")


national_data = queries.get_precovid_totals()


national_data["Unemployment Rate"] = national_data["Unemployment"] / national_data["Labor Force"]
national_data["Unemployment Rate Change"] = national_data["Unemployment Rate"].shift(1)
national_data["Unemployment Rate Change"] = national_data["Unemployment Rate Change"] - national_data["Unemployment Rate"]
national_data

national_data["Date"] = pd.to_datetime(national_data["Date"])
national_data["Month"] = national_data["Date"].dt.month_name()
average_year = national_data.groupby("Month")["Unemployment Rate Change"].mean().reset_index()

average_year["Month"] = pd.Categorical(average_year["Month"], categories=months_order, ordered=True)

charts.good_bar_chart(average_year, "Month", "Unemployment Rate Change", sort_order = months_order, y_format="%")



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


    chart = alt.Chart(data).mark_point(size=100, filled=True, opacity=1).encode(
        x=alt.X("Month:N", axis=alt.Axis(labelColor="#0A3161", titleColor="#0A3161"), sort=months_order),
        y=alt.Y("Unemployment Rate Change:Q", axis=alt.Axis(labelColor="#0A3161", titleColor="#0A3161", format="%"), 
                scale=alt.Scale()),
        color="State/Area:N",
    ) + alt.Chart(data).mark_line(strokeDash=[5,5], opacity=0.6).encode(
        x=alt.X("Month:N", axis=alt.Axis(labelColor="#0A3161", titleColor="#0A3161"), sort=months_order),
        y=alt.Y("Unemployment Rate Change:Q", axis=alt.Axis(labelColor="#0A3161", titleColor="#0A3161", format="%"), 
                scale=alt.Scale()),
        color="State/Area:N",
    ) 

    st.altair_chart(chart, use_container_width=True)

