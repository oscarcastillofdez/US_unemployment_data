import streamlit as st
import pandas as pd
import sidebar
import queries

sidebar.config()
st.set_page_config(
    page_title="Empleo en EE. UU.",
    page_icon="🇺🇸",
    layout="wide"
    )
users, groups, roles, gp, gr = queries.get_all_users_tables()
st.write(users)
st.write(groups)
st.write(roles)
st.write(gp)
st.write(gr)