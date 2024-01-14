import streamlit as st

from app import app
from login import create_credentials, register_widget
import streamlit_authenticator as stauth

st.set_page_config(
    layout="wide", page_title="Stock Analyser", initial_sidebar_state="collapsed"
)

conn = st.connection("sql")

if "authenticator" not in st.session_state:
    st.session_state.authenticator = stauth.Authenticate(
        create_credentials(conn), "login_info", "tanveer singh bedi", 30
    )


def signin_signup_widget():
    if not st.session_state["authentication_status"]:
        login, register = st.tabs(["Sign in", "Sign up"])

        with login:
            _, authentication_status, _ = st.session_state.authenticator.login(
                "Sign In", "main"
            )

        with register:
            register_widget(conn, "Sign Up")

        return authentication_status


signin_signup_widget()

if st.session_state["authentication_status"] == False:
    st.error("Username/password is incorrect")
elif st.session_state["authentication_status"] == True:
    st.session_state.authenticator.logout("Logout", "sidebar")
    app(conn)

