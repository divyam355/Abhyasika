import streamlit as st
import pandas as pd
from datetime import date
from core.database import Database

db = Database()


def calculate_accuracy(score, total):

    if total == 0:
        return 0

    return round((score / total) * 100, 2)


def show(exam):

    st.title(f"📝 Mock Tests - {exam[1]}")

    st.divider()

    subjects = db.get_subjects(exam[0])

    if len(subjects) == 0:

        st.warning(
            "Please add subjects before creating mock tests."
        )

        return

    subject_names = [s[2] for s in subjects]

    with st.expander("➕ Add Mock Test", expanded=False):

        left, right = st.columns(2)

        with left:

            subject_name = st.selectbox(
                "Subject",
                subject_names
            )

            selected_subject = None

            for s in subjects:

                if s[2] == subject_name:
                    selected_subject = s

                    break

            topics = db.get_topics(selected_subject[0])

            topic_names = [t[2] for t in topics]

            if len(topic_names) == 0:
                topic_names = ["No Topics"]

            topic_name = st.selectbox(
                "Topic",
                topic_names
            )

            test_name = st.text_input(
                "Mock Test Name"
            )

        with right:

            score = st.number_input(
                "Marks Obtained",
                min_value=0.0,
                value=0.0
            )

            total = st.number_input(
                "Total Marks",
                min_value=1.0,
                value=100.0
            )

            time_taken = st.number_input(
                "Time Taken (Minutes)",
                min_value=1,
                value=180
            )

            test_date = st.date_input(
                "Test Date",
                value=date.today()
            )

        accuracy = calculate_accuracy(
            score,
            total
        )

        st.metric(
            "Accuracy",
            f"{accuracy}%"
        )

        save = st.button(
            "💾 Save Mock Test",
            use_container_width=True
        )

        if save:

            if test_name.strip() == "":

                st.error("Mock Test Name is required.")

            elif topic_name == "No Topics":

                st.error("Please create a topic first.")

            else:

                selected_topic = None

                for t in topics:

                    if t[2] == topic_name:
                        selected_topic = t

                        break

                db.add_mock_test(

                    exam[0],

                    selected_subject[0],

                    selected_topic[0],

                    test_name,

                    score,

                    total,

                    accuracy,

                    time_taken,

                    str(test_date)

                )

                st.success("Mock Test Added Successfully")

                st.rerun()

            with right:

                score = st.number_input(
                    "Marks Obtained",
                    min_value=0.0,
                    value=0.0
                )

                total = st.number_input(
                    "Total Marks",
                    min_value=1.0,
                    value=100.0
                )

                time_taken = st.number_input(
                    "Time Taken (Minutes)",
                    min_value=1,
                    value=180
                )

                test_date = st.date_input(
                    "Test Date",
                    value=date.today()
                )

            accuracy = calculate_accuracy(
                score,
                total
            )

            st.metric(
                "Accuracy",
                f"{accuracy}%"
            )

            save = st.form_submit_button(
                "💾 Save Mock Test",
                use_container_width=True
            )

            if save:

                if test_name.strip() == "":

                    st.error(
                        "Mock Test Name is required."
                    )

                elif topic_name == "No Topics":

                    st.error(
                        "Please create a topic first."
                    )

                else:

                    selected_topic = None

                    for t in topics:

                        if t[2] == topic_name:

                            selected_topic = t

                            break

                    db.add_mock_test(

                        exam[0],

                        selected_subject[0],

                        selected_topic[0],

                        test_name,

                        score,

                        total,

                        accuracy,

                        time_taken,

                        str(test_date)

                    )

                    st.success(
                        "Mock Test Added Successfully"
                    )

                    st.rerun()

    st.divider()

    mock_tests = db.get_mock_tests(
        exam[0]
    )

    if len(mock_tests) == 0:

        st.info("No Mock Tests Added Yet")

        return

    df = pd.DataFrame(
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

    average_score = round(df["Score"].mean(), 2)

    highest_score = round(df["Score"].max(), 2)

    lowest_score = round(df["Score"].min(), 2)

    average_accuracy = round(df["Accuracy"].mean(), 2)

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Average Score",
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

    st.subheader("📈 Performance Trend")

    chart = df.set_index("Test Name")["Score"]

    st.line_chart(chart)

    st.divider()

    st.subheader("📋 Mock Test History")

    for test in mock_tests:

        mock_id = test[0]

        with st.container(border=True):

            left, right = st.columns([3,1])

            with left:
                subject_name = db.get_subject_name(test[2])

                topic_name = db.get_topic_name(test[3])

                st.markdown(f"### 📝 {test[4]}")

                st.caption(f"📚 {subject_name}")

                st.caption(f"📖 {topic_name}")

                st.progress(test[7] / 100)

                c1, c2 = st.columns(2)

                with c1:
                    st.metric(
                        "Score",
                        f"{test[5]} / {test[6]}"
                    )

                    st.metric(
                        "Accuracy",
                        f"{test[7]}%"
                    )

                with c2:
                    st.metric(
                        "Time",
                        f"{test[8]} Min"
                    )

                    st.metric(
                        "Date",
                        test[9]
                    )

            with right:

                st.metric(
                    "Accuracy",
                    f"{test[7]}%"
                )

                if st.button(
                    "🗑 Delete",
                    key=f"mock_{mock_id}",
                    use_container_width=True
                ):

                    db.delete_mock_test(
                        mock_id
                    )

                    st.success(
                        "Mock Test Deleted"
                    )

                    st.rerun()

    st.divider()

    st.subheader("📊 Complete Performance Table")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )