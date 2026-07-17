import streamlit as st

from core.database import Database
from auth.security import Security
from auth.session import login

db = Database()


def show():

    st.title("📚 Abhyasika")

    st.subheader("Welcome Back")

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    # =====================================================
    # LOGIN
    # =====================================================

    with tab1:

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login"):

            if not username or not password:

                st.warning("Please enter username and password.")

            else:

                user = db.get_user_by_username(username)

                st.write("User from DB:", user)

                if user is None:

                    st.error("Invalid username or password.")

                else:

                    # Database columns:
                    # 0 = user_id
                    # 1 = full_name
                    # 2 = username
                    # 3 = email
                    # 4 = mobile
                    # 5 = password
                    # 6 = role

                    stored_password = user[5]

                    if Security.verify_password(password, stored_password):

                        login(user)

                        st.success("Login Successful!")

                        st.rerun()

                    else:

                        st.error("Invalid username or password.")

    # =====================================================
    # REGISTER
    # =====================================================

    with tab2:

        full_name = st.text_input(
            "Full Name"
        )

        username = st.text_input(
            "Username"
        )

        email = st.text_input(
            "Email"
        )

        mobile = st.text_input(
            "Mobile"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Create Account"):

            if password != confirm:

                st.error("Passwords do not match.")

            elif (
                    not full_name or
                    not username or
                    not email or
                    not password
            ):

                st.warning("Please fill all required fields.")

            else:

                try:

                    hashed_password = Security.hash_password(password)

                    db.register_user(
                        full_name,
                        username,
                        email,
                        mobile,
                        hashed_password
                    )

                    st.success("Account created successfully! Please login.")

                except Exception as e:

                    st.error(f"Registration failed: {e}")
