from core.database import Database

db = Database()


def build_context(exam=None):

    context = ""

    # -----------------------------------
    # Dashboard Statistics
    # -----------------------------------

    subjects = db.get_subject_count()
    topics = db.get_topic_count()
    completed = db.get_completed_topic_count()
    mocks = db.get_mock_test_count()
    notes = db.get_note_count()

    if topics == 0:
        progress = 0
    else:
        progress = round(
            (completed / topics) * 100,
            2
        )

    context += f"""
Overall Progress

Subjects : {subjects}

Topics : {topics}

Completed Topics : {completed}

Progress : {progress} %

Mock Tests : {mocks}

Notes : {notes}

"""

    # -----------------------------------
    # Exam Details
    # -----------------------------------

    if exam is not None:

        context += f"""

Current Exam

Name : {exam[1]}

Organization : {exam[2]}

"""

        context += "\nSubjects\n"

        subject_list = db.get_subjects(exam[0])

        for subject in subject_list:

            subject_id = subject[0]

            context += f"\n📘 {subject[2]}\n"

            topic_list = db.get_topics(subject_id)

            for topic in topic_list:

                status = "❌"

                try:

                    if topic[3] == 1:
                        status = "✅"

                except:

                    pass

                context += f"{status} {topic[2]}\n"

    return context
