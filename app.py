import streamlit as st

from matplotlib.colors import LinearSegmentedColormap

import login
import home

def logout():
    st.session_state.dev = False
    st.session_state.admin = False
    st.session_state.exec = False
    st.session_state.logged_in = False

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login.layout()
else:
    home.layout()
    st.button("Cerrar Sesión", on_click=logout)



    

    
