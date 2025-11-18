import streamlit as st

def config():
    st.sidebar.page_link('app.py', label='Summary')
    st.sidebar.page_link('Pages/state_analysis.py', label='State Analysis')
    st.sidebar.page_link('Pages/prediction.py', label='Prediction')
    st.sidebar.page_link('Pages/typical_year.py', label='Average year')
    if st.session_state.admin or st.session_state.dev:
        st.sidebar.page_link('Pages/data.py', label='Data')
    if st.session_state.admin:
        st.sidebar.page_link('Pages/users.py', label='Users')

    st.set_page_config(
        page_title="USA Employment",
        page_icon="🇺🇸",
        layout="wide"
    )

    