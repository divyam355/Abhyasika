import streamlit as st
import pandas as pd
from datetime import date
from core.database import Database

db = Database()


def show(exam):

    st.title(f"📅 Calendar - {exam[1]}")

    st.divider()

    st.subheader("➕ Add Event")

    with st.form("calendar_form"):

        title = st.text_input(
            "Event Title"
        )

        event_type = st.selectbox(

            "Event Type",

            [

                "Registration",

                "Fee Payment",

                "Admit Card",

                "Exam",

                "Result",

                "Study",

                "Revision",

                "Personal"

            ]

        )

        event_date = st.date_input(

            "Event Date",

            value=date.today()

        )

        description = st.text_area(

            "Description"

        )

        save = st.form_submit_button(

            "💾 Save Event",

            use_container_width=True

        )

        if save:

            if title.strip() == "":

                st.error(
                    "Please enter event title."
                )

            else:

                db.add_calendar_event(

                    exam[0],

                    title,

                    event_type,

                    str(event_date),

                    description

                )

                st.success(
                    "Event Added Successfully"
                )

                st.rerun()

    st.divider()

    # =====================================================
    # UPCOMING EVENTS
    # =====================================================

    events = db.get_calendar_events(exam[0])

    st.subheader("📌 Upcoming Events")

    if len(events) == 0:

        st.info("No Events Available.")

    else:

        today = date.today()

        for event in events:

            event_id = event[0]

            title = event[2]

            event_type = event[3]

            event_date = date.fromisoformat(event[4])

            description = event[5]

            remaining = (event_date - today).days

            with st.container(border=True):

                c1, c2 = st.columns([5,1])

                with c1:

                    st.markdown(f"### {title}")

                    st.caption(event_type)

                    st.write(description)

                    if remaining > 1:

                        st.info(
                            f"⏳ {remaining} Days Remaining"
                        )

                    elif remaining == 1:

                        st.warning(
                            "⚠ Tomorrow"
                        )

                    elif remaining == 0:

                        st.error(
                            "🔥 Today"
                        )

                    else:

                        st.success(
                            "✅ Completed"
                        )

                with c2:

                    st.metric(
                        "Date",
                        str(event_date)
                    )

                    if st.button(
                        "🗑 Delete",
                        key=f"event_{event_id}",
                        use_container_width=True
                    ):

                        db.delete_calendar_event(
                            event_id
                        )

                        st.success(
                            "Event Deleted"
                        )

                        st.rerun()

    st.divider()
    # =====================================================
    # CALENDAR DASHBOARD
    # =====================================================

    st.subheader("📊 Calendar Overview")

    total_events = len(events)

    upcoming = 0
    today_events = 0
    completed = 0

    today = date.today()

    for event in events:

        event_date = date.fromisoformat(event[4])

        if event_date > today:

            upcoming += 1

        elif event_date == today:

            today_events += 1

        else:

            completed += 1

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Total Events",
            total_events
        )

    with c2:

        st.metric(
            "Upcoming",
            upcoming
        )

    with c3:

        st.metric(
            "Today",
            today_events
        )

    with c4:

        st.metric(
            "Completed",
            completed
        )

    st.divider()

    # =====================================================
    # TODAY'S EVENTS
    # =====================================================

    st.subheader("📅 Today's Schedule")

    found = False

    for event in events:

        event_date = date.fromisoformat(event[4])

        if event_date == today:

            found = True

            st.success(
                f"{event[3]} • {event[2]}"
            )

            if event[5] != "":

                st.caption(event[5])

    if not found:

        st.info("No events today.")

    st.divider()

    # =====================================================
    # NEXT 7 DAYS
    # =====================================================

    st.subheader("⏳ Next 7 Days")

    found = False

    for event in events:

        event_date = date.fromisoformat(event[4])

        remaining = (event_date - today).days

        if 1 <= remaining <= 7:

            found = True

            st.warning(
                f"{event[2]} • {remaining} day(s) remaining"
            )

    if not found:

        st.success(
            "Nothing scheduled for the next 7 days."
        )

    st.divider()

    # =====================================================
    # COMPLETE EVENT TABLE
    # =====================================================

    st.subheader("📋 Event History")

    if len(events) > 0:

        df = pd.DataFrame(

            events,

            columns=[

                "ID",

                "Exam ID",

                "Title",

                "Type",

                "Date",

                "Description",

                "Created"

            ]

        )

        st.dataframe(

            df,

            hide_index=True,

            use_container_width=True

        )