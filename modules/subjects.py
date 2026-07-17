import streamlit as st
from core.database import Database

db = Database()


def show(exam):

    st.title(f"📚 Subjects - {exam[1]}")

    st.divider()

    with st.expander("➕ Add Subject", expanded=False):

        with st.form("add_subject"):

            subject_name = st.text_input(
                "Subject Name"
            )

            save = st.form_submit_button(
                "Save Subject",
                use_container_width=True
            )

            if save:

                if subject_name.strip() == "":

                    st.error("Enter Subject Name")

                else:

                    db.add_subject(
                        exam[0],
                        subject_name
                    )

                    st.success("Subject Added")

                    st.rerun()

    st.divider()

    subjects = db.get_subjects(exam[0])

    if len(subjects) == 0:

        st.info("No Subjects Added")

        return

    for subject in subjects:

        subject_id = subject[0]
        subject_name = subject[2]

        with st.container(border=True):

            left, right = st.columns([4, 1])

            with left:

                total_topics = db.get_total_topics(subject_id)

                completed_topics = db.get_completed_topics(subject_id)

                if total_topics == 0:
                    progress = 0
                else:
                    progress = round((completed_topics / total_topics) * 100)

                st.subheader(f"📘 {subject_name}")

                st.progress(progress / 100)

                st.caption(
                    f"{completed_topics} / {total_topics} Topics Completed ({progress}%)"
                )

            with right:

                if st.button(
                    "📂 Open",
                    key=f"subject_open_{subject_id}",
                    use_container_width=True
                ):

                    st.session_state.selected_subject = subject

                    st.session_state.workspace = "topics"

                    st.rerun()

                if st.button(
                    "🗑 Delete",
                    key=f"subject_delete_{subject_id}",
                    use_container_width=True
                ):

                    db.delete_subject(subject_id)

                    st.success("Subject Deleted")

                    st.rerun()