import streamlit as st
from modules.subjects import show as subjects_page
from modules.topics import show as topics_page
from modules.mock_tests import show as mock_page
from modules.analytics import show as analytics_page
from modules.calendar import show as calendar_page
from modules.ai_coach import show as ai_page

def show(exam):

    # -----------------------------
    # Initialize Workspace State
    # -----------------------------

    if "workspace" not in st.session_state:
        st.session_state.workspace = "dashboard"

    if "selected_subject" not in st.session_state:
        st.session_state.selected_subject = None

    # -----------------------------
    # Header
    # -----------------------------

    st.title(f"📘 {exam[1]}")

    st.caption("Exam Workspace")

    st.divider()

    # -----------------------------
    # Navigation Buttons
    # -----------------------------

    row1 = st.columns(3)

    with row1[0]:

        if st.button(
            "🏠 Dashboard",
            use_container_width=True
        ):
            st.session_state.workspace = "dashboard"
            st.rerun()

    with row1[1]:

        if st.button(
            "📚 Subjects",
            use_container_width=True
        ):
            st.session_state.workspace = "subjects"
            st.rerun()

    with row1[2]:

        if st.button(
            "📝 Mock Tests",
            use_container_width=True
        ):
            st.session_state.workspace = "mock"
            st.rerun()

    row2 = st.columns(3)

    with row2[0]:

        if st.button(
            "📖 Notes",
            use_container_width=True
        ):
            st.session_state.workspace = "notes"
            st.rerun()

    with row2[1]:

        if st.button(
            "📅 Calendar",
            use_container_width=True
        ):
            st.session_state.workspace = "calendar"
            st.rerun()

    with row2[2]:

        if st.button(
            "📊 Analytics",
            use_container_width=True
        ):
            st.session_state.workspace = "analytics"
            st.rerun()

    st.divider()



    # -----------------------------
    # Workspace Routing
    # -----------------------------

    if st.session_state.workspace == "dashboard":

        st.info(
            "Welcome to your exam workspace.\n\n"
            "Choose a module above to continue."
        )

    elif st.session_state.workspace == "subjects":

        subjects_page(exam)

    elif st.session_state.workspace == "topics":

        if st.session_state.selected_subject is None:

            st.warning(
                "Please open a subject first."
            )

        else:

            topics_page(
                st.session_state.selected_subject
            )


    elif st.session_state.workspace == "mock":

        mock_page(exam)


    elif st.session_state.workspace == "notes":

        st.info("📖 Notes Module Coming Soon")


    elif st.session_state.workspace == "calendar":

        calendar_page(exam)


    elif st.session_state.workspace == "analytics":

        analytics_page(exam)
