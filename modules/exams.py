import streamlit as st
from datetime import date
from core.database import Database

db = Database()


# ======================================================
# REGISTRATION STATUS
# ======================================================

def get_registration_status(reg_start, reg_end, exam_date):

    today = date.today()

    if today < reg_start:
        return "🔵 Upcoming"

    elif reg_start <= today <= reg_end:
        return "🟢 Registration Open"

    elif reg_end < today < exam_date:
        return "🟠 Registration Closed"

    elif today == exam_date:
        return "🔴 Exam Today"

    else:
        return "⚫ Completed"


# ======================================================
# FEE STATUS
# ======================================================

def get_fee_status(fee_last_date):

    today = date.today()

    if today < fee_last_date:

        days = (fee_last_date - today).days

        if days == 0:
            return "🟠 Ends Today"

        return f"🟢 {days} Days Left"

    elif today == fee_last_date:

        return "🔴 Last Day"

    else:

        return "⚫ Closed"


# ======================================================
# COUNTDOWN
# ======================================================

def get_countdown(exam_date):

    today = date.today()

    if exam_date >= today:
        return (exam_date - today).days

    return 0


# ======================================================
# EXAM FILTER
# ======================================================

def get_exam_group(reg_start, exam_date):

    today = date.today()

    if today < reg_start:
        return "Upcoming"

    elif reg_start <= today <= exam_date:
        return "Ongoing"

    else:
        return "Completed"


# ======================================================
# MAIN PAGE
# ======================================================

def show():

    st.title("📝 Exam Management")

    left, right = st.columns([3, 1])

    with left:

        search = st.text_input(
            "🔍 Search Exam",
            placeholder="Search by Exam Name..."
        )

    with right:

        sort_by = st.selectbox(
            "Sort",
            [
                "Exam Date",
                "Name"
            ]
        )

    tab_all, tab_upcoming, tab_ongoing, tab_completed = st.tabs(

        [
            "🟢 All",

            "🔵 Upcoming",

            "🟠 Ongoing",

            "⚫ Completed"

        ]

    )

    st.divider()

    with st.expander("➕ Add New Exam", expanded=False):

        with st.form("add_exam"):

            col1, col2 = st.columns(2)

            with col1:

                exam_name = st.text_input("Exam Name *")

                organization = st.text_input("Organization")

                official_website = st.text_input("Official Website")

                category = st.selectbox(

                    "Category",

                    [

                        "GATE",

                        "ESE",

                        "CAT",

                        "UPSC",

                        "SSC",

                        "Bank",

                        "Defence",

                        "Other"

                    ]

                )

                exam_mode = st.selectbox(

                    "Exam Mode",

                    [

                        "Online",

                        "Offline",

                        "Hybrid"

                    ]

                )

                priority = st.selectbox(

                    "Priority",

                    [

                        "High",

                        "Medium",

                        "Low"

                    ]

                )

                fee = st.number_input(

                    "Application Fee",

                    min_value=0.0,

                    step=100.0

                )

            with col2:

                registration_start = st.date_input(

                    "Registration Start"

                )

                registration_end = st.date_input(

                    "Registration End"

                )

                fee_last_date = st.date_input(

                    "Fee Submission Last Date"

                )

                correction_date = st.date_input(

                    "Correction Date"

                )

                admit_card_date = st.date_input(

                    "Admit Card Date"

                )

                exam_date = st.date_input(

                    "Exam Date"

                )

                answer_key_date = st.date_input(

                    "Answer Key Date"

                )

                result_date = st.date_input(

                    "Result Date"

                )

            remarks = st.text_area(

                "Remarks"

            )

            save = st.form_submit_button(

                "💾 Save Exam",

                use_container_width=True

            )

            if save:

                st.write("DEBUG: Save button clicked")

                if exam_name.strip() == "":

                    st.error("Exam Name is required.")

                elif st.session_state.user_id is None:

                    st.error("User ID is missing. Please logout and login again.")

                else:

                    try:

                        st.write(
                            f"DEBUG: Current User ID = {st.session_state.user_id}"
                        )

                        exam_data = {

                            "user_id": st.session_state.user_id,

                            "exam_name": exam_name,
                            "organization": organization,
                            "official_website": official_website,
                            "category": category,
                            "exam_mode": exam_mode,
                            "priority": priority,
                            "fee": fee,

                            "registration_start": str(registration_start),
                            "registration_end": str(registration_end),
                            "fee_last_date": str(fee_last_date),
                            "correction_date": str(correction_date),
                            "admit_card_date": str(admit_card_date),
                            "exam_date": str(exam_date),
                            "answer_key_date": str(answer_key_date),
                            "result_date": str(result_date),

                            "remarks": remarks
                        }

                        db.add_exam(exam_data)

                        st.success("Exam Added Successfully!")

                        st.write("DEBUG: Database insert completed")

                    except Exception as e:

                        st.error(
                            f"Failed to save exam: {type(e).__name__}: {e}"
                        )

    all_exams = db.get_all_exams(
        st.session_state.user_id
    )
    # ======================================================
    # DISPLAY EXAMS
    # ======================================================

    def display_exam_cards(exam_list, section):

        if len(exam_list) == 0:
            st.info("No exams found.")
            return

        for exam in exam_list:

            exam_id = exam["exam_id"]
            user_id = exam["user_id"]

            exam_name = exam["exam_name"]
            organization = exam["organization"]
            website = exam["official_website"]

            category = exam["category"]
            mode = exam["exam_mode"]
            priority = exam["priority"]

            fee = exam["fee"]

            registration_start = date.fromisoformat(exam["registration_start"])
            registration_end = date.fromisoformat(exam["registration_end"])
            fee_last_date = date.fromisoformat(exam["fee_last_date"])
            correction_date = date.fromisoformat(exam["correction_date"])
            admit_card_date = date.fromisoformat(exam["admit_card_date"])
            exam_date = date.fromisoformat(exam["exam_date"])
            answer_key_date = date.fromisoformat(exam["answer_key_date"])
            result_date = date.fromisoformat(exam["result_date"])

            remarks = exam["remarks"] or ""

            registration_status = get_registration_status(
                registration_start,
                registration_end,
                exam_date
            )

            fee_status = get_fee_status(
                fee_last_date
            )

            countdown = get_countdown(
                exam_date
            )

            with st.container(border=True):

                top_left, top_right = st.columns([4, 1])

                with top_left:

                    st.markdown(f"## 📘 {exam_name}")

                    st.caption(organization)

                with top_right:

                    st.metric(
                        "Countdown",
                        f"{countdown} Days"
                    )

                info1, info2, info3 = st.columns(3)

                with info1:

                    st.metric(
                        "Registration",
                        registration_status
                    )

                with info2:

                    st.metric(
                        "Fee",
                        fee_status
                    )

                with info3:

                    st.metric(
                        "Priority",
                        priority
                    )

                st.divider()

                left, right = st.columns([2, 1])

                with left:

                    st.markdown("#### 📅 Important Dates")

                    st.write(
                        f"**Registration :** {registration_start} → {registration_end}"
                    )

                    st.write(
                        f"**Fee Submission :** {fee_last_date}"
                    )

                    st.write(
                        f"**Correction :** {correction_date}"
                    )

                    st.write(
                        f"**Admit Card :** {admit_card_date}"
                    )

                    st.write(
                        f"**Exam :** {exam_date}"
                    )

                    st.write(
                        f"**Answer Key :** {answer_key_date}"
                    )

                    st.write(
                        f"**Result :** {result_date}"
                    )

                with right:

                    st.markdown("#### ℹ Information")

                    st.write(f"**Category :** {category}")

                    st.write(f"**Mode :** {mode}")

                    st.write(f"**Fee :** ₹ {fee}")

                    if website:
                        st.link_button(
                            "🌐 Official Website",
                            website,
                            use_container_width=True
                        )

                if remarks:

                    st.info(f"📝 {remarks}")

                b1, b2, b3 = st.columns(3)

                with b1:

                    if st.button(
                            "📂 Open Workspace",
                            key=f"{section}_open_{exam_id}",
                            use_container_width=True
                    ):
                        st.session_state.selected_exam = exam
                        st.session_state.page = "workspace"

                        st.rerun()

                with b2:

                    st.button(
                        "✏ Edit",
                        key=f"{section}_edit_{exam_id}",
                        use_container_width=True
                    )

                with b3:

                    if st.button(
                        "🗑 Delete",
                        key=f"{section}_delete_{exam_id}",
                        use_container_width=True
                    ):

                        db.delete_exam(exam_id)

                        st.success("Exam Deleted")

                        st.rerun()
    # ======================================================
    # FILTER EXAMS
    # ======================================================

    filtered_all = []
    upcoming = []
    ongoing = []
    completed = []

    for exam in all_exams:

        # Search Filter
        if search:
            if search.lower() not in exam["exam_name"].lower():
                continue

        # Category
        exam_group = get_exam_group(
            date.fromisoformat(exam["registration_start"]),
            date.fromisoformat(exam["exam_date"])
        )

        filtered_all.append(exam)

        if exam_group == "Upcoming":
            upcoming.append(exam)

        elif exam_group == "Ongoing":
            ongoing.append(exam)

        else:
            completed.append(exam)

    # ======================================================
    # SORTING
    # ======================================================

    if sort_by == "Exam Date":

        filtered_all.sort(key=lambda x: x["exam_date"])
        upcoming.sort(key=lambda x: x["exam_date"])
        ongoing.sort(key=lambda x: x["exam_date"])
        completed.sort(key=lambda x: x["exam_date"])

    else:

        filtered_all.sort(key=lambda x: x["exam_name"].lower())
        upcoming.sort(key=lambda x: x["exam_name"].lower())
        ongoing.sort(key=lambda x: x["exam_name"].lower())
        completed.sort(key=lambda x: x["exam_name"].lower())

    # ======================================================
    # DISPLAY
    # ======================================================

    with tab_all:

        display_exam_cards(
            filtered_all,
            "all"
        )

    with tab_upcoming:

        display_exam_cards(
            upcoming,
            "upcoming"
        )

    with tab_ongoing:

        display_exam_cards(
            ongoing,
            "ongoing"
        )

    with tab_completed:

        display_exam_cards(
            completed,
            "completed"
        )