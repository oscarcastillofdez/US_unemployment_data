import streamlit as st
import queries
import sidebar
import altair as alt
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd

def layout():

    sidebar.config()
    st.set_page_config(
    page_title="Empleo en EE. UU.",
    page_icon="🇺🇸",
    layout="wide"
    )

    st.write("# 🇺🇸 Datos de Empleo 1976-2022")


    national_data = queries.get_national_totals()

    national_data["Inactive Population"] = national_data["Non-Institutional Population"] - national_data["Labor Force"]
    national_data["Labor Force Rate"] = national_data["Labor Force"] / national_data["Non-Institutional Population"]
    national_data["Employment Rate"] = national_data["Employment"] / national_data["Non-Institutional Population"]
    national_data["Unemployment Rate"] = national_data["Unemployment"] / national_data["Labor Force"]
    national_data = national_data.rename(columns={"Date":"Fecha", "Employment Rate":"Empleo", "Unemployment Rate":"Desempleo"})


    chart_desempleo = (
            alt.Chart(national_data)
            .mark_area(color="#B31942")
            .encode(
                x=alt.X("Fecha:T", title=None),
                y=alt.Y("Desempleo:Q", axis=alt.Axis(format='%'), stack=None, title=None)
            )
        )

    chart_empleo= (
            alt.Chart(national_data)
            .mark_line(color="#0A3161")
            .encode(
                x=alt.X("Fecha:T",title=None),
                y=alt.Y("Empleo:Q", axis=alt.Axis(format='%'), stack=None, scale= alt.Scale(domain=[0.45, 0.7]), title=None)

            )
        )

    average_data = queries.get_state_average()

    average_data["Employment Rate"] = average_data["Employment"] / average_data["Non-Institutional Population"]
    average_data["Unemployment Rate"] = average_data["Unemployment"] / average_data["Labor Force"]

    employment_average = average_data.drop(columns=["FIPS Code", "Labor Force", "Employment", "Unemployment", "Non-Institutional Population", "Unemployment Rate"])
    unemployment_average = average_data.drop(columns=["FIPS Code", "Labor Force", "Employment", "Unemployment", "Non-Institutional Population", "Employment Rate"])

    employment_average = employment_average.sort_values(by="Employment Rate", ascending=False)
    unemployment_average = unemployment_average.sort_values(by="Unemployment Rate")

    employment_average = employment_average.reset_index(drop=True)
    unemployment_average = unemployment_average.reset_index(drop=True)

    employment_average.index = employment_average.index + 1
    unemployment_average.index = unemployment_average.index + 1

    employment_average = employment_average.rename(columns={"State/Area":"Estado", "Employment Rate":"Empleo"})
    unemployment_average = unemployment_average.rename(columns={"State/Area":"Estado", "Unemployment Rate":"Desempleo"})

    employment_style = employment_average.style.format({"Empleo":"{:.2%}"})
    unemployment_style = unemployment_average.style.format({"Desempleo":"{:.2%}"})

    employment_cmap = LinearSegmentedColormap.from_list("employment_gradient", ["white", "#8598B0", "#0A3161"])
    unemployment_cmap = LinearSegmentedColormap.from_list("unemployment_gradient", ["white", "#D98CA1", "#B31942"])

    employment_style = employment_style.background_gradient(subset=["Empleo"], cmap=employment_cmap)
    unemployment_style = unemployment_style.background_gradient(subset=["Desempleo"], cmap=unemployment_cmap)

    nl_df = pd.concat([queries.get_latest_national_data(), queries.get_national_average()])
    nl_df.index = ["Actual", "Promedio"]
    nl_df["Labor Force Rate"] = nl_df["Labor Force"] / nl_df["Non-Institutional Population"]
    nl_df["Employment Rate"] = nl_df["Employment"] / nl_df["Non-Institutional Population"]
    nl_df["Unemployment Rate"] = nl_df["Unemployment"] / nl_df["Labor Force"]
    nl_df = nl_df.drop(columns=["Labor Force", "Employment", "Unemployment"])
    nl_df["Non-Institutional Population"] = nl_df["Non-Institutional Population"].round().astype(int)
    nl_df["Labor Force Rate"] = nl_df["Labor Force Rate"].apply(lambda x: f"{x*100:.2f}%")
    nl_df["Employment Rate"] = nl_df["Employment Rate"].apply(lambda x: f"{x*100:.2f}%")
    nl_df["Unemployment Rate"] = nl_df["Unemployment Rate"].apply(lambda x: f"{x*100:.2f}%")
    nl_df = nl_df.rename(columns={"Non-Institutional Population":"Población Apta", "Labor Force Rate":"Población Activa", "Employment Rate":"Empleo", "Unemployment Rate":"Desempleo"})
    st.write(nl_df)

    col11, col12 = st.columns([2,1])

    with col11:
        st.write("## Porcentaje de Desempleo")
        st.write("")
        st.write("")
        st.altair_chart(chart_desempleo, use_container_width=True)
        
        
    with col12:
        st.write("#### Ranking de Estados por Desempleo Promedio")
        st.write(unemployment_style)
        
    col21, col22 = st.columns([2,1])

    with col21:
        st.write("## Porcentaje de Empleo")
        st.write("")
        st.write("")
        st.altair_chart(chart_empleo, use_container_width=True)

    with col22:
        st.write("#### Ranking de Estados por Empleo Promedio")
        st.write(employment_style)