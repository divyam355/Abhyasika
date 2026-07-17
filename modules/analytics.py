import streamlit as st
import pandas as pd
from core.database import Database

db = Database()


def show(exam):

    st.title(f"📊 Analytics - {exam[1]}")

    st.divider()

    # -----------------------------
    # Basic Counts
    # -----------------------------

    subjects = db.get_subjects(exam[0])

    total_subjects = len(subjects)

    total_topics = 0
    completed_topics = 0

    for subject in subjects:

        sid = subject[0]

        total_topics += db.get_total_topics(sid)

        completed_topics += db.get_completed_topics(sid)

    if total_topics == 0:

        progress = 0

    else:

        progress = round(
            (completed_topics / total_topics) * 100,
            2
        )

    mock_tests = db.get_mock_tests(exam[0])

    total_mock_tests = len(mock_tests)

    # -----------------------------
    # KPI Cards
    # -----------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Subjects",
            total_subjects
        )

    with c2:

        st.metric(
            "Topics",
            total_topics
        )

    with c3:

        st.metric(
            "Completed",
            completed_topics
        )

    with c4:

        st.metric(
            "Progress",
            f"{progress}%"
        )

    st.divider()

    # =====================================================
    # OVERALL STUDY PROGRESS
    # =====================================================

    st.subheader("📈 Overall Study Progress")

    st.progress(progress / 100)

    st.write(
        f"### {progress}% Completed"
    )

    st.caption(
        f"{completed_topics} / {total_topics} Topics Completed"
    )

    st.divider()

    # =====================================================
    # SUBJECT WISE PROGRESS
    # =====================================================

    st.subheader("📚 Subject Wise Progress")

    if total_subjects == 0:

        st.info("No subjects available.")

    else:

        progress_data = []

        for subject in subjects:

            subject_id = subject[0]

            subject_name = subject[2]

            total = db.get_total_topics(subject_id)

            completed = db.get_completed_topics(subject_id)

            if total == 0:

                percentage = 0

            else:

                percentage = round(
                    (completed / total) * 100,
                    2
                )

            progress_data.append(
                [
                    subject_name,
                    completed,
                    total,
                    percentage
                ]
            )

            with st.container(border=True):

                st.write(f"### 📘 {subject_name}")

                st.progress(percentage / 100)

                st.caption(
                    f"{completed} / {total} Topics Completed"
                )

                st.metric(
                    "Progress",
                    f"{percentage}%"
                )

        st.divider()

        # =====================================================
        # SUBJECT TABLE
        # =====================================================

        st.subheader("📋 Subject Summary")

        df_subject = pd.DataFrame(

            progress_data,

            columns=[
                "Subject",
                "Completed",
                "Total",
                "Progress (%)"
            ]
        )

        st.dataframe(
            df_subject,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # =====================================================
    # MOCK TEST ANALYTICS
    # =====================================================

    st.subheader("📝 Mock Test Analytics")

    if total_mock_tests == 0:

        st.info("No Mock Tests Available.")

    else:

        df_mock = pd.DataFrame(

            mock_tests,

            columns=[
                "ID",
                "Exam ID",
                "Subject ID",
                "Topic ID",
                "Test Name",
                "Score",
                "Total",
                "Accuracy",
                "Time",
                "Test Date",
                "Created At"
            ]
        )

        average_score = round(
            df_mock["Score"].mean(),
            2
        )

        highest_score = round(
            df_mock["Score"].max(),
            2
        )

        lowest_score = round(
            df_mock["Score"].min(),
            2
        )

        average_accuracy = round(
            df_mock["Accuracy"].mean(),
            2
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Average",
                average_score
            )

        with c2:

            st.metric(
                "Highest",
                highest_score
            )

        with c3:

            st.metric(
                "Lowest",
                lowest_score
            )

        with c4:

            st.metric(
                "Accuracy",
                f"{average_accuracy}%"
            )

        st.divider()

        st.subheader("📈 Score Trend")

        chart = df_mock.set_index("Test Name")["Score"]

        st.line_chart(chart)

        st.divider()

    # =====================================================
    # STRONG & WEAK SUBJECTS
    # =====================================================

    st.subheader("🎯 Subject Analysis")

    if len(progress_data) == 0:

        st.info("No Subjects Found.")

    else:

        strong = []

        weak = []

        for row in progress_data:

            if row[3] >= 70:

                strong.append(row)

            elif row[3] <= 40:

                weak.append(row)

        left, right = st.columns(2)

        with left:

            st.success("🏆 Strong Subjects")

            if len(strong) == 0:

                st.write("No Strong Subjects")

            else:

                for row in strong:

                    st.write(
                        f"✅ {row[0]} ({row[3]}%)"
                    )

        with right:

            st.error("⚠ Needs Improvement")

            if len(weak) == 0:

                st.write("No Weak Subjects")

            else:

                for row in weak:

                    st.write(
                        f"🔴 {row[0]} ({row[3]}%)"
                    )

    st.divider()

    # =====================================================
    # DAILY TARGET
    # =====================================================

    st.subheader("🎯 Daily Target")

    remaining = total_topics - completed_topics

    if remaining == 0:

        st.success(
            "🎉 Congratulations! All Topics Completed."
        )

    else:

        days = st.number_input(

            "Days Remaining Until Exam",

            min_value=1,

            value=30
        )

        target = remaining / days

        st.metric(

            "Topics Per Day",

            round(target, 2)

        )

        st.progress(
            progress / 100
        )

        st.caption(
            f"{remaining} Topics Remaining"
        )

    st.divider()

    # =====================================================
    # COMPLETE ANALYTICS TABLE
    # =====================================================

    st.subheader("📊 Analytics Summary")

    summary = pd.DataFrame(

        [

            ["Subjects", total_subjects],

            ["Topics", total_topics],

            ["Completed Topics", completed_topics],

            ["Remaining Topics", remaining],

            ["Progress", f"{progress}%"],

            ["Mock Tests", total_mock_tests]

        ],

        columns=[

            "Metric",

            "Value"

        ]

    )

    st.dataframe(

        summary,

        use_container_width=True,

        hide_index=True

    )