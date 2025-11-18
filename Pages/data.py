import streamlit as st
from Utils import queries
from Utils import config_page

config_page.config()

state, date, data = queries.get_all_data_tables()
st.write(state)
st.write(date)
st.write(data)
