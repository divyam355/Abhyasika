import streamlit as st


def initialize_session():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if "username" not in st.session_state:
        st.session_state.username = None

    if "role" not in st.session_state:
        st.session_state.role = None


def login(user):

    st.session_state.logged_in = True

    st.session_state.user_id = user[0]

    st.session_state.username = user[2]

    st.session_state.role = user[6]


def logout():

    st.session_state.logged_in = False

    st.session_state.user_id = None

    st.session_state.username = None

    st.session_state.role = None

    st.rerun()