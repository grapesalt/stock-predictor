import streamlit as st
import streamlit_authenticator as stauth

from sqlalchemy import text


def users_from_db(conn):
    df = conn.query("SELECT * FROM USERS", ttl=600)

    usernames = []
    passwords = []
    emails = []
    names = []

    for row in df.itertuples():
        usernames.append(row[1])
        passwords.append(row[2])
        names.append(row[3])
        emails.append(row[4])

    return zip(usernames, passwords, emails, names)


def register_user(conn, username, password, name, email):
    with conn.session as s:
        s.execute(
            text(
                f'INSERT INTO USERS VALUE("{username}", "{password}", "{name}", "{email}");'
            )
        )
        s.commit()

def create_credentials(conn):
    users = users_from_db(conn)
    return {
            "usernames": {
                username: {
                    "email": email,
                    "name": name,
                    "password": password,
                }
                for username, password, name, email in users
            }
        }

def register_widget(conn, display_name):
    if not st.session_state["authentication_status"]:
        try:
            if st.session_state.authenticator.register_user(display_name, preauthorization=False):
                users = st.session_state.authenticator.credentials["usernames"]
                username, values = list(users.items())[-1]
                register_user(
                    conn, username, values["password"], values["name"], values["email"]
                )
                st.success("User registered successfully")
        except Exception as e:
            st.error(e)
