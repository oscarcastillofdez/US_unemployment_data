import sidebar
import streamlit as st
import queries

sidebar.config()
st.set_page_config(
    page_title="Empleo en EE. UU.",
    page_icon="🇺🇸",
    layout="wide"
    )
state, date, data = queries.get_all_data_tables()
st.write(state)
st.write(date)
st.write(data)
