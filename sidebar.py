import streamlit as st

def config():
    st.sidebar.page_link('app.py', label='Resumen')
    st.sidebar.page_link('pages/Analisis_Estatal.py', label='Analisis Estatal')
    st.sidebar.page_link('pages/Analisis_Predictivo.py', label='Predicción')
    st.sidebar.page_link('pages/Anho tipico.py', label='Año típico')
    if st.session_state.admin or st.session_state.dev:
        st.sidebar.page_link('pages/Datos.py', label='Datos')
    if st.session_state.admin:
        st.sidebar.page_link('pages/Usuarios.py', label='Usuarios')
    

    