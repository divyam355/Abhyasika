import sqlite3
from pathlib import Path


class Database:

    def __init__(self):

        project_root = Path(__file__).resolve().parent.parent

        database_folder = project_root / "database"

        database_folder.mkdir(parents=True, exist_ok=True)

        self.db_path = database_folder / "abhyasika.db"

    # ==========================================================
    # CONNECTION
    # ==========================================================

    import sqlite3

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # ==========================================================
    # CREATE TABLES
    # ==========================================================

    def create_tables(self):

        conn = self.connect()

        cursor = conn.cursor()

        # ======================================================
        # USERS
        # ======================================================

        # ======================================================
        # USERS
        # ======================================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            mobile TEXT,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)





        # ======================================================
        # EXAMS
        # ======================================================

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS exams(

            exam_id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            exam_name TEXT NOT NULL,

            organization TEXT,

            official_website TEXT,

            category TEXT,

            exam_mode TEXT,

            priority TEXT,

            fee REAL,

            registration_start TEXT,

            registration_end TEXT,

            fee_last_date TEXT,

            correction_date TEXT,

            admit_card_date TEXT,

            exam_date TEXT,

            answer_key_date TEXT,

            result_date TEXT,

            remarks TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)

        # ======================================================
        # SUBJECTS
        # ======================================================

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS subjects(

            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,

            exam_id INTEGER,

            subject_name TEXT,

            completed INTEGER DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)

        # ======================================================
        # TOPICS
        # ======================================================

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS topics(

            topic_id INTEGER PRIMARY KEY AUTOINCREMENT,

            subject_id INTEGER,

            topic_name TEXT,

            completed INTEGER DEFAULT 0,

            revision_count INTEGER DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)

        # ======================================================
        # MOCK TESTS
        # ======================================================

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS mock_tests(

            mock_id INTEGER PRIMARY KEY AUTOINCREMENT,

            exam_id INTEGER,

            subject_id INTEGER,

            topic_id INTEGER,

            test_name TEXT,

            score REAL,

            total_marks REAL,

            accuracy REAL,

            time_taken INTEGER,

            test_date TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)

        # ======================================================
        # NOTES
        # ======================================================

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS notes(

            note_id INTEGER PRIMARY KEY AUTOINCREMENT,

            exam_id INTEGER,

            subject_id INTEGER,

            topic_id INTEGER,

            title TEXT,

            note_type TEXT,

            file_path TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)

        # ======================================================
        # CALENDAR
        # ======================================================

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS calendar(

            calendar_id INTEGER PRIMARY KEY AUTOINCREMENT,

            exam_id INTEGER,

            title TEXT,

            event_type TEXT,

            event_date TEXT,

            description TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)

        # ======================================================
        # ANALYTICS
        # ======================================================

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS analytics(

            analytics_id INTEGER PRIMARY KEY AUTOINCREMENT,

            exam_id INTEGER,

            subject_id INTEGER,

            completed_topics INTEGER,

            total_topics INTEGER,

            study_hours REAL,

            last_updated TEXT

        )

        """)

        conn.commit()

        conn.close()

    # ==========================================================
    # ADD EXAM
    # ==========================================================

    def add_exam(self, exam):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO exams(

                user_id,
                exam_name,
                organization,
                official_website,
                category,
                exam_mode,
                priority,
                fee,
                registration_start,
                registration_end,
                fee_last_date,
                correction_date,
                admit_card_date,
                exam_date,
                answer_key_date,
                result_date,
                remarks

            )

            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

        """, (

            exam["user_id"],
            exam["exam_name"],
            exam["organization"],
            exam["official_website"],
            exam["category"],
            exam["exam_mode"],
            exam["priority"],
            exam["fee"],
            exam["registration_start"],
            exam["registration_end"],
            exam["fee_last_date"],
            exam["correction_date"],
            exam["admit_card_date"],
            exam["exam_date"],
            exam["answer_key_date"],
            exam["result_date"],
            exam["remarks"]

        ))

        conn.commit()
        conn.close()


    # ==========================================================
    # GET ALL EXAMS
    # ==========================================================

    # ==========================================================
    # GET ALL EXAMS FOR USER
    # ==========================================================

    def get_all_exams(self, user_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM exams
            WHERE user_id = ?
            ORDER BY exam_date
            """,
            (user_id,)
        )

        exams = cursor.fetchall()

        conn.close()

        return exams
    # ==========================================================
    # DELETE EXAM
    # ==========================================================

    def delete_exam(self, exam_id):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(

            """

            DELETE

            FROM exams

            WHERE exam_id=?

            """,

            (exam_id,)

        )

        conn.commit()

        conn.close()


    # ==========================================================
    # EXAM COUNT
    # ==========================================================

    def get_exam_count(self):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(

            "SELECT COUNT(*) FROM exams"

        )

        count = cursor.fetchone()[0]

        conn.close()

        return count

    # ==========================================================
    # ADD SUBJECT
    # ==========================================================

    def add_subject(self, exam_id, subject_name):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO subjects(
                exam_id,
                subject_name
            )
            VALUES(?,?)
            """,
            (
                exam_id,
                subject_name
            )
        )

        conn.commit()
        conn.close()


    # ==========================================================
    # GET SUBJECTS
    # ==========================================================

    def get_subjects(self, exam_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM subjects
            WHERE exam_id=?
            ORDER BY subject_name
            """,
            (exam_id,)
        )

        data = cursor.fetchall()

        conn.close()

        return data


    # ==========================================================
    # DELETE SUBJECT
    # ==========================================================

    def delete_subject(self, subject_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM subjects
            WHERE subject_id=?
            """,
            (subject_id,)
        )

        conn.commit()
        conn.close()


    # ==========================================================
    # ADD TOPIC
    # ==========================================================

    def add_topic(self, subject_id, topic_name):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO topics(
                subject_id,
                topic_name
            )
            VALUES(?,?)
            """,
            (
                subject_id,
                topic_name
            )
        )

        conn.commit()
        conn.close()


    # ==========================================================
    # GET TOPICS
    # ==========================================================

    def get_topics(self, subject_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM topics
            WHERE subject_id=?
            ORDER BY topic_name
            """,
            (subject_id,)
        )

        data = cursor.fetchall()

        conn.close()

        return data


    # ==========================================================
    # DELETE TOPIC
    # ==========================================================

    def delete_topic(self, topic_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM topics
            WHERE topic_id=?
            """,
            (topic_id,)
        )

        conn.commit()
        conn.close()


    # ==========================================================
    # DATABASE HEALTH CHECK
    # ==========================================================

    def test_connection(self):

        try:

            conn = self.connect()
            conn.close()

            return True

        except Exception:

            return False

    # ==========================================================
    # GET SUBJECT NAME
    # ==========================================================

    def get_subject_name(self, subject_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT subject_name FROM subjects WHERE subject_id=?",
            (subject_id,)
        )

        row = cursor.fetchone()

        conn.close()

        if row:
            return row[0]

        return "Unknown"

    # ==========================================================
    # GET TOPIC NAME
    # ==========================================================

    def get_topic_name(self, topic_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT topic_name FROM topics WHERE topic_id=?",
            (topic_id,)
        )

        row = cursor.fetchone()

        conn.close()

        if row:
            return row[0]

        return "Unknown"
    # ==========================================================
    # ADD MOCK TEST
    # ==========================================================

    def add_mock_test(
        self,
        exam_id,
        subject_id,
        topic_id,
        test_name,
        score,
        total_marks,
        accuracy,
        time_taken,
        test_date
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO mock_tests(
                exam_id,
                subject_id,
                topic_id,
                test_name,
                score,
                total_marks,
                accuracy,
                time_taken,
                test_date
            )
            VALUES(?,?,?,?,?,?,?,?,?)
        """, (
            exam_id,
            subject_id,
            topic_id,
            test_name,
            score,
            total_marks,
            accuracy,
            time_taken,
            test_date
        ))

        conn.commit()
        conn.close()


    # ==========================================================
    # GET MOCK TESTS
    # ==========================================================

    def get_mock_tests(self, exam_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM mock_tests
            WHERE exam_id=?
            ORDER BY test_date DESC
        """, (exam_id,))

        data = cursor.fetchall()

        conn.close()

        return data


    # ==========================================================
    # DELETE MOCK TEST
    # ==========================================================

    def delete_mock_test(self, mock_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM mock_tests WHERE mock_id=?",
            (mock_id,)
        )

        conn.commit()
        conn.close()


    # ==========================================================
    # UPDATE TOPIC STATUS
    # ==========================================================

    def update_topic_status(self, topic_id, completed):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE topics
            SET completed=?
            WHERE topic_id=?
            """,
            (
                completed,
                topic_id
            )
        )

        conn.commit()
        conn.close()


    # ==========================================================
    # COMPLETED TOPICS
    # ==========================================================

    def get_completed_topics(self, subject_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM topics
            WHERE subject_id=?
            AND completed=1
            """,
            (subject_id,)
        )

        count = cursor.fetchone()[0]

        conn.close()

        return count

    # ==========================================================
    # TOTAL TOPICS OF SUBJECT
    # ==========================================================

    def get_total_topics(self, subject_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM topics
            WHERE subject_id=?
            """,
            (subject_id,)
        )

        total = cursor.fetchone()[0]

        conn.close()

        return total

    # ==========================================================
    # TOTAL SUBJECTS
    # ==========================================================

    def get_subject_count(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM subjects"
        )

        count = cursor.fetchone()[0]

        conn.close()

        return count


    # ==========================================================
    # TOTAL TOPICS
    # ==========================================================

    def get_topic_count(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM topics"
        )

        count = cursor.fetchone()[0]

        conn.close()

        return count


    # ==========================================================
    # TOTAL COMPLETED TOPICS
    # ==========================================================

    def get_completed_topic_count(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM topics
            WHERE completed=1
            """
        )

        count = cursor.fetchone()[0]

        conn.close()

        return count


    # ==========================================================
    # TOTAL MOCK TESTS
    # ==========================================================

    def get_mock_test_count(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM mock_tests"
        )

        count = cursor.fetchone()[0]

        conn.close()

        return count


    # ==========================================================
    # TOTAL NOTES
    # ==========================================================

    def get_note_count(self):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM notes"
        )

        count = cursor.fetchone()[0]

        conn.close()

        return count

    # ==========================================================
    # ADD CALENDAR EVENT
    # ==========================================================

    def add_calendar_event(

        self,

        exam_id,

        title,

        event_type,

        event_date,

        description

    ):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute("""

            INSERT INTO calendar(

                exam_id,

                title,

                event_type,

                event_date,

                description

            )

            VALUES(?,?,?,?,?)

        """, (

            exam_id,

            title,

            event_type,

            event_date,

            description

        ))

        conn.commit()

        conn.close()

    # ==========================================================
    # GET CALENDAR EVENTS
    # ==========================================================

    def get_calendar_events(self, exam_id):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute("""

            SELECT *

            FROM calendar

            WHERE exam_id=?

            ORDER BY event_date

        """, (exam_id,))

        data = cursor.fetchall()

        conn.close()

        return data

    # ==========================================================
    # DELETE CALENDAR EVENT
    # ==========================================================

    def delete_calendar_event(self, event_id):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(

            "DELETE FROM calendar WHERE calendar_id=?",

            (event_id,)

        )

        conn.commit()

        conn.close()

        # ==========================================================
        # REGISTER USER
        # ==========================================================

        def register_user(
                self,
                full_name,
                username,
                email,
                mobile,
                password,
                role="user"
        ):
            conn = self.connect()
            cursor = conn.cursor()

            cursor.execute("""
                    INSERT INTO users(
                        full_name,
                        username,
                        email,
                        mobile,
                        password,
                        role
                    )
                    VALUES(?,?,?,?,?,?)
                """, (
                full_name,
                username,
                email,
                mobile,
                password,
                role
            ))

            conn.commit()
            conn.close()

    # ==========================================================
    # REGISTER USER
    # ==========================================================

    def register_user(
        self,
        full_name,
        username,
        email,
        mobile,
        password,
        role="user"
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users(
                full_name,
                username,
                email,
                mobile,
                password,
                role
            )
            VALUES(?,?,?,?,?,?)
        """, (
            full_name,
            username,
            email,
            mobile,
            password,
            role
        ))

        conn.commit()
        conn.close()


    # ==========================================================
    # GET USER BY USERNAME
    # ==========================================================

    def get_user_by_username(self, username):

        conn = self.connect()
        cursor = conn.cursor()

        # Show all users in the table
        cursor.execute("SELECT * FROM users")
        print("ALL USERS:", cursor.fetchall())

        # Search for the entered username
        cursor.execute("""
            SELECT *
            FROM users
            WHERE username=?
        """, (username,))

        user = cursor.fetchone()

        conn.close()

        return user


    # ==========================================================
    # GET USER BY ID
    # ==========================================================

    def get_user_by_id(self, user_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE user_id = ?
        """, (user_id,))

        user = cursor.fetchone()

        conn.close()

        return user


