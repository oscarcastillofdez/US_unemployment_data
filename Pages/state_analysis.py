import streamlit as st
import pandas as pd
import altair as alt
from Utils import queries
from Utils import config_page

config_page.config()

all_data = queries.get_all_data()

national = queries.get_national_totals()
national["State/Area"] = "Total"
national["FIPS Code"] = "00"

all_data = all_data.drop(columns="Unemployment Rate")
all_data = pd.concat([all_data, national])

states_df = queries.get_state_data()
states_df.loc[len(states_df)] = ["00", "Total"]

states = st.multiselect("Choose states", list(states_df["State/Area"]), ["Iowa"])

all_data["Inactive Population"] = all_data["Non-Institutional Population"] - all_data["Labor Force"]
all_data["Labor Force Rate"] = all_data["Labor Force"] / all_data["Non-Institutional Population"]
all_data["Employment Rate"] = all_data["Employment"] / all_data["Non-Institutional Population"]
all_data["Unemployment Rate"] = all_data["Unemployment"] / all_data["Labor Force"]

measures_list = list(all_data.columns)

measures_list.remove("FIPS Code")
measures_list.remove("Date")
measures_list.remove("State/Area")


measure = st.selectbox("Measure", measures_list)

not_measure = measures_list

not_measure.remove(measure)

all_data = all_data.drop(columns=not_measure)



if not states:
    st.error("Choose a state.")
else:
    all_data = all_data.set_index("State/Area")
    data = all_data.loc[states]

    data = data.reset_index()

    pivoted_data = data.pivot(index="State/Area", columns="Date", values=measure)
    pivoted_data.sort_index()


    st.write(pivoted_data)

    chart = (
        alt.Chart(data)
        .mark_area(opacity=0.3)
        .encode(
            x="Date:T",
            y=alt.Y(measure, stack=None),
            color="State/Area:N",
        )
    )
    st.altair_chart(chart, use_container_width=True)