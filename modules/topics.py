import streamlit as st
from core.database import Database

db = Database()


def show(subject):

    st.title(f"📖 {subject[2]}")

    st.divider()

    with st.expander("➕ Add Topic", expanded=False):

        with st.form("topic_form"):

            topic_name = st.text_input(
                "Topic Name"
            )

            save = st.form_submit_button(
                "💾 Save Topic",
                use_container_width=True
            )

            if save:

                if topic_name.strip() == "":

                    st.error("Enter Topic Name")

                else:

                    db.add_topic(
                        subject[0],
                        topic_name
                    )

                    st.success("Topic Added Successfully")

                    st.rerun()

    st.divider()

    topics = db.get_topics(subject[0])

    if len(topics) == 0:

        st.info("No Topics Added")

        return

    for topic in topics:

        topic_id = topic[0]
        topic_name = topic[2]
        completed = bool(topic[3])

        with st.container(border=True):

            col1, col2 = st.columns([5, 1])

            with col1:

                checked = st.checkbox(
                    topic_name,
                    value=completed,
                    key=f"topic_{topic_id}"
                )

                if checked != completed:
                    db.update_topic_status(
                        topic_id,
                        int(checked)
                    )

                    st.rerun()

            with col2:

                if st.button(
                        "🗑",
                        key=f"delete_{topic_id}",
                        use_container_width=True
                ):
                    db.delete_topic(topic_id)

                    st.rerun()