import streamlit as st
import queries

def login():

    username = st.session_state.username
    password = st.session_state.password

    password_df = queries.get_user_password(username)

    if (len(password_df) != 1):
        st.error("Usuario o contraseña incorrectos")
    elif password_df.loc[0, "user_password"] == password:
        st.session_state.logged_in = True

        roles_df = queries.get_roles(username)

        roles_flags = {rol: (rol in list(roles_df["role_name"])) for rol in ["administrator", "developer", "executive"]}

        st.session_state.admin = roles_flags.get("administrator")
        st.session_state.exec = roles_flags.get("executive")
        st.session_state.dev = roles_flags.get("developer")
        
    else:
        st.error("Usuario o contraseña incorrectos")

def layout():
    st.set_page_config(page_title="Login", page_icon="🔑", layout="centered")

    st.title("🔐 Página de Login")
    st.text_input("Usuario", key="username")
    st.text_input("Contraseña", type="password", key="password")

    st.button("Iniciar sesión", on_click=login)

