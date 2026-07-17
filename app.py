import streamlit as st

from core.database import Database
from core.styles import load_css
from auth.session import initialize_session
from auth.login import show as login_page

from modules.dashboard import show as dashboard_page
from modules.exams import show as exams_page
from modules.workspace import show as workspace_page
from modules.ai_coach import show as ai_page

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Abhyasika",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- SESSION STATE ---------------- #

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

if "workspace" not in st.session_state:
    st.session_state.workspace = "dashboard"

if "selected_exam" not in st.session_state:
    st.session_state.selected_exam = None

if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = None

# ---------------- DATABASE ---------------- #

db = Database()
db.create_tables()

# ---------------- SESSION ---------------- #

initialize_session()

# ---------------- CSS ---------------- #

load_css()

# ---------------- LOGIN ---------------- #

if not st.session_state.logged_in:

    login_page()

    st.stop()
# ---------------- SIDEBAR ---------------- #

st.sidebar.title("📚 Abhyasika")
st.sidebar.caption("AI Powered Exam Management Platform")

st.sidebar.divider()

page = st.sidebar.radio(

    "Navigation",

    [

        "🏠 Dashboard",

        "📝 Exams",

        "📅 Calendar",

        "📝 Notes",

        "🤖 AI Coach",

        "⚙ Settings"

    ]

)

st.sidebar.divider()

st.sidebar.info("Version 0.1")

# ---------------- ROUTING ---------------- #

# If user selects Exams and has opened an exam workspace
if page == "📝 Exams":

    if (
        st.session_state.page == "workspace"
        and st.session_state.selected_exam is not None
    ):

        workspace_page(
            st.session_state.selected_exam
        )

    else:

        exams_page()


elif page == "🏠 Dashboard":

    # Reset workspace navigation
    st.session_state.page = "dashboard"

    dashboard_page()


elif page == "📅 Calendar":

    st.session_state.page = "dashboard"

    st.title("📅 Calendar")

    st.info(
        "Please open an Exam first."
    )


elif page == "📝 Notes":

    st.session_state.page = "dashboard"

    st.title("📝 Notes")

    st.info(
        "Please open an Exam first."
    )


elif page == "🤖 AI Coach":

    st.session_state.page = "dashboard"

    ai_page(
        st.session_state.selected_exam
    )


elif page == "⚙ Settings":

    st.session_state.page = "dashboard"

    st.title("⚙ Settings")

    st.info(
        "Module Under Development"
    )