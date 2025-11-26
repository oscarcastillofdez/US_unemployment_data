import streamlit as st
import pandas as pd
import altair as alt
from matplotlib.colors import LinearSegmentedColormap
from Utils import queries
from Utils import charts
from Utils import config_page

def layout():

    config_page.config()

    st.write("# 🇺🇸 Employment Data 1976-2022")


    national_data = queries.get_national_totals()

    national_data["Inactive Population"] = national_data["Non-Institutional Population"] - national_data["Labor Force"]
    national_data["Labor Force Rate"] = national_data["Labor Force"] / national_data["Non-Institutional Population"]
    national_data["Employment Rate"] = national_data["Employment"] / national_data["Non-Institutional Population"]
    national_data["Unemployment Rate"] = national_data["Unemployment"] / national_data["Labor Force"]

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

    employment_style = employment_average.style.format({"Employment Rate":"{:.2%}"})
    unemployment_style = unemployment_average.style.format({"Unemployment Rate":"{:.2%}"})

    employment_cmap = LinearSegmentedColormap.from_list("employment_gradient", ["white", "#8598B0", "#0A3161"])
    unemployment_cmap = LinearSegmentedColormap.from_list("unemployment_gradient", ["white", "#D98CA1", "#B31942"])

    employment_style = employment_style.background_gradient(subset=["Employment Rate"], cmap=employment_cmap)
    unemployment_style = unemployment_style.background_gradient(subset=["Unemployment Rate"], cmap=unemployment_cmap)

    nl_df = pd.concat([queries.get_latest_national_data(), queries.get_national_average()])
    nl_df.index = ["Current", "Average"]
    nl_df["Labor Force Rate"] = nl_df["Labor Force"] / nl_df["Non-Institutional Population"]
    nl_df["Employment Rate"] = nl_df["Employment"] / nl_df["Non-Institutional Population"]
    nl_df["Unemployment Rate"] = nl_df["Unemployment"] / nl_df["Labor Force"]
    nl_df = nl_df.drop(columns=["Labor Force", "Employment", "Unemployment"])
    nl_df["Non-Institutional Population"] = nl_df["Non-Institutional Population"].round().astype(int)
    nl_df["Labor Force Rate"] = nl_df["Labor Force Rate"].apply(lambda x: f"{x*100:.2f}%")
    nl_df["Employment Rate"] = nl_df["Employment Rate"].apply(lambda x: f"{x*100:.2f}%")
    nl_df["Unemployment Rate"] = nl_df["Unemployment Rate"].apply(lambda x: f"{x*100:.2f}%")
    st.write(nl_df)

    col11, col12 = st.columns([2,1])

    with col11:
        st.write("## Unemployment Rate")
        st.write("")
        st.write("")
        charts.red_area_chart(national_data, "Date", "Unemployment Rate", y_format="%")
        
        
    with col12:
        st.write("#### Average Unemployment Rate Ranking")
        st.write(unemployment_style)
        
    col21, col22 = st.columns([2,1])

    with col21:
        st.write("## Employment Rate")
        st.write("")
        st.write("")
        charts.blue_line_chart(national_data, "Date", "Employment Rate", y_format="%")


    with col22:
        st.write("#### Average Employment Rate Ranking")
        st.write(employment_style)