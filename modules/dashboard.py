import streamlit as st
from datetime import date
from core.database import Database

db = Database()


# ======================================================
# METRIC CARD
# ======================================================

def metric_card(title, value):

    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">{title}</div>
            <div class="card-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ======================================================
# MAIN DASHBOARD
# ======================================================

def show():

    # --------------------------------------------------
    # Get Logged-In User
    # --------------------------------------------------

    user_id = st.session_state.user_id

    # --------------------------------------------------
    # Get User Exams
    # --------------------------------------------------

    exams = db.get_all_exams(user_id)

    total_exams = len(exams)

    # --------------------------------------------------
    # Dashboard Statistics
    # --------------------------------------------------

    subject_count = db.get_subject_count()

    topic_count = db.get_topic_count()

    completed_topics = db.get_completed_topic_count()

    mock_count = db.get_mock_test_count()

    note_count = db.get_note_count()

    # --------------------------------------------------
    # Calculate Study Progress
    # --------------------------------------------------

    if topic_count == 0:

        progress = 0

    else:

        progress = round(
            (completed_topics / topic_count) * 100
        )

    # --------------------------------------------------
    # Exam Statistics
    # --------------------------------------------------

    today = date.today()

    upcoming = 0

    ongoing = 0

    completed = 0

    alerts = []

    for exam in exams:

        registration_start = date.fromisoformat(
            exam["registration_start"]
        )

        registration_end = date.fromisoformat(
            exam["registration_end"]
        )

        fee_last_date = date.fromisoformat(
            exam["fee_last_date"]
        )

        exam_date = date.fromisoformat(
            exam["exam_date"]
        )

        # ----------------------------------------------
        # Exam Status
        # ----------------------------------------------

        if today < registration_start:

            upcoming += 1

        elif registration_start <= today <= exam_date:

            ongoing += 1

        else:

            completed += 1

        # ----------------------------------------------
        # Registration Alert
        # ----------------------------------------------

        days = (
            registration_end - today
        ).days

        if 0 <= days <= 7:

            alerts.append(
                f"📝 {exam['exam_name']} "
                f"Registration closes in {days} day(s)"
            )

        # ----------------------------------------------
        # Fee Alert
        # ----------------------------------------------

        days = (
            fee_last_date - today
        ).days

        if 0 <= days <= 7:

            alerts.append(
                f"💰 {exam['exam_name']} "
                f"Fee Payment in {days} day(s)"
            )

        # ----------------------------------------------
        # Exam Alert
        # ----------------------------------------------

        days = (
            exam_date - today
        ).days

        if 0 <= days <= 15:

            alerts.append(
                f"📅 {exam['exam_name']} "
                f"Exam in {days} day(s)"
            )

    # ==================================================
    # HEADER
    # ==================================================

    st.markdown(
        '<div class="main-title">📚 Abhyasika</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Exam Preparation Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # ==================================================
    # TOP CARDS
    # ==================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        metric_card(
            "Total Exams",
            total_exams
        )

    with c2:

        metric_card(
            "Upcoming",
            upcoming
        )

    with c3:

        metric_card(
            "Ongoing",
            ongoing
        )

    with c4:

        metric_card(
            "Completed",
            completed
        )

    st.write("")

    left, right = st.columns(
        [2, 1]
    )

    # ==================================================
    # LEFT SIDE
    # ==================================================

    with left:

        # ----------------------------------------------
        # Upcoming Alerts
        # ----------------------------------------------

        st.markdown(
            """
            <div class="section">
            <h3>🔔 Upcoming Alerts</h3>
            """,
            unsafe_allow_html=True
        )

        if len(alerts) == 0:

            st.success(
                "No alerts for the next few days."
            )

        else:

            for alert in alerts:

                st.write(alert)

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

        st.write("")

        # ----------------------------------------------
        # Study Progress
        # ----------------------------------------------

        st.markdown(
            """
            <div class="section">
            <h3>📈 Study Progress</h3>
            """,
            unsafe_allow_html=True
        )

        st.progress(
            progress / 100
        )

        st.write(
            f"### {progress}% Completed"
        )

        st.caption(
            f"{completed_topics} / "
            f"{topic_count} Topics Completed"
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    # ==================================================
    # RIGHT SIDE
    # ==================================================

    with right:

        st.markdown(
            """
            <div class="section">
            <h3>📊 Quick Statistics</h3>
            """,
            unsafe_allow_html=True
        )

        st.metric(
            "Subjects",
            subject_count
        )

        st.metric(
            "Topics",
            topic_count
        )

        st.metric(
            "Mock Tests",
            mock_count
        )

        st.metric(
            "Notes",
            note_count
        )

        st.metric(
            "Completion",
            f"{progress}%"
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    st.write("")

    # ==================================================
    # RECENT ACTIVITY
    # ==================================================

    st.markdown(
        """
        <div class="section">
        <h3>📝 Recent Activity</h3>
        """,
        unsafe_allow_html=True
    )

    if total_exams == 0:

        st.info(
            "No recent activity."
        )

    else:

        latest = exams[-1]

        st.success(
            f"Latest Exam Added : "
            f"{latest['exam_name']}"
        )

        st.write(
            f"Organization : "
            f"{latest['organization']}"
        )

        st.write(
            f"Exam Date : "
            f"{latest['exam_date']}"
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )