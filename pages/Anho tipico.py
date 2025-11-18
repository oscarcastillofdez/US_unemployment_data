import sidebar
import streamlit as st
import pandas as pd
import queries
import altair as alt

sidebar.config()
st.set_page_config(
    page_title="Empleo en EE. UU.",
    page_icon="🇺🇸",
    layout="wide"
    )


def good_chart(df, x, y):

    chart = alt.Chart(df).mark_bar().encode(
        x=x,
        y=alt.Y(y, scale=alt.Scale())
    )

    st.altair_chart(chart, use_container_width=True)

df = queries.get_average_change_year()
df2 = queries.get_average_year()

meses = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

df["mes_nombre"] = df["Month"].map(meses)
df2["mes_nombre"] = df2["Month"].map(meses)

orden_meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

df["mes_nombre"] = pd.Categorical(df["mes_nombre"], categories=orden_meses, ordered=True)
df2["mes_nombre"] = pd.Categorical(df["mes_nombre"], categories=orden_meses, ordered=True)

df.set_index("mes_nombre")
df2.set_index("mes_nombre")

good_chart(df, "mes_nombre", "Non-Institutional Population Change")
good_chart(df, "mes_nombre", "Labor Force Change")
good_chart(df, "mes_nombre", "Employment Change")
good_chart(df, "mes_nombre", "Unemployment Change")
st.write("# Esta esta mal")
good_chart(df, "mes_nombre", "Unemployment Rate Change")

#good_chart(df2, "mes_nombre", "Non-Institutional Population")
#good_chart(df2, "mes_nombre", "Labor Force")
#good_chart(df2, "mes_nombre", "Employment")
#good_chart(df2, "mes_nombre", "Unemployment")

national_data = queries.get_precovid_totals()


national_data["Unemployment Rate"] = national_data["Unemployment"] / national_data["Labor Force"]
national_data["Unemployment Rate Change"] = national_data["Unemployment Rate"].shift(1)
national_data["Unemployment Rate Change"] = national_data["Unemployment Rate Change"] - national_data["Unemployment Rate"]

national_data["Date"] = pd.to_datetime(national_data["Date"])
national_data["mes"] = national_data["Date"].dt.month
national_data["mes_nombre"] = national_data["Date"].dt.month_name(locale="es_ES")
media_por_mes = national_data.groupby("mes_nombre")["Unemployment Rate Change"].mean().reset_index()

media_por_mes["mes_nombre"] = pd.Categorical(df["mes_nombre"], categories=orden_meses, ordered=True)

media_por_mes = media_por_mes.sort_values("mes_nombre")

good_chart(media_por_mes, "mes_nombre", "Unemployment Rate Change")



#national_data = queries.get_all_data()
#national_data = national_data.sort_values(["State/Area", "Date"])
#national_data["Unemployment Rate Change"] = national_data.groupby("State/Area")["Unemployment Rate"].shift(1)
#st.write(national_data)


