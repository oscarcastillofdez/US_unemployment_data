import streamlit as st
import pandas as pd
from Utils import config_page
from Utils import queries

config_page.config()
users, groups, roles, gp, gr = queries.get_all_users_tables()
st.write(users)
st.write(groups)
st.write(roles)
st.write(gp)
st.write(gr)