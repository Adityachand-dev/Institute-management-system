import sqlite3
from datetime import datetime

DB_NAME = "institute.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin(
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO admin(username,password)
    VALUES('admin','admin123')
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        gender TEXT,
        dob TEXT,
        mobile TEXT UNIQUE,
        email TEXT,
        address TEXT,
        course TEXT,
        batch TEXT,
        admission_date TEXT,
        course_fee REAL,
        fee_paid REAL DEFAULT 0,
        balance_fee REAL
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses(
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT UNIQUE,
        duration TEXT,
        fees REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS batches(
        batch_id INTEGER PRIMARY KEY AUTOINCREMENT,
        batch_name TEXT,
        timing TEXT,
        course_name TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        status TEXT,
        FOREIGN KEY(student_id)
        REFERENCES students(student_id)
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fee_payments(
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        payment_date TEXT,
        amount REAL,
        FOREIGN KEY(student_id)
        REFERENCES students(student_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs(
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity TEXT,
        log_time TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_log(activity):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO logs(activity, log_time)
    VALUES(?,?)
    """, (activity, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database Created Successfully.")


def add_student(data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students(
        full_name,
        gender,
        dob,
        mobile,
        email,
        address,
        course,
        batch,
        admission_date,
        course_fee,
        fee_paid,
        balance_fee
    )
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
    """, data)

    conn.commit()

    student_id = cursor.lastrowid

    add_log(f"Student Added : ID {student_id}")

    conn.close()

    return student_id

def search_student(student_id=None, mobile=None):

    conn = get_connection()
    cursor = conn.cursor()

    if student_id:
        cursor.execute(
            "SELECT * FROM students WHERE student_id=?",
            (student_id,)
        )

    elif mobile:
        cursor.execute(
            "SELECT * FROM students WHERE mobile=?",
            (mobile,)
        )

    else:
        conn.close()
        return None

    student = cursor.fetchone()
    conn.close()

    return student

def update_student(data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE students SET

        full_name=?,
        gender=?,
        dob=?,
        mobile=?,
        email=?,
        address=?,
        course=?,
        batch=?,
        course_fee=?,
        fee_paid=?,
        balance_fee=?

    WHERE student_id=?

    """, data)

    conn.commit()

    add_log(f"Student Updated : ID {data[-1]}")

    conn.close()

def delete_student(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE student_id=?",
        (student_id,)
    )

    conn.commit()

    add_log(f"Student Deleted : ID {student_id}")

    conn.close()

def get_all_students():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM students
    ORDER BY student_id
    """)

    students = cursor.fetchall()

    conn.close()

    return students

def add_course(course_name, duration, fees):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO courses(course_name,duration,fees)
    VALUES(?,?,?)
    """,(course_name,duration,fees))

    conn.commit()

    add_log(f"Course Added : {course_name}")

    conn.close()


def update_course(course_id, course_name, duration, fees):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE courses
    SET course_name=?, duration=?, fees=?
    WHERE course_id=?
    """,(course_name,duration,fees,course_id))

    conn.commit()

    add_log(f"Course Updated : {course_name}")

    conn.close()


def get_courses():

    conn=get_connection()

    cursor=conn.cursor()

    cursor.execute("""
    SELECT * FROM courses
    ORDER BY course_name
    """)

    courses=cursor.fetchall()

    conn.close()

    return courses

def add_batch(batch_name, timing, course_name):

    conn=get_connection()

    cursor=conn.cursor()

    cursor.execute("""
    INSERT INTO batches(
    batch_name,
    timing,
    course_name
    )
    VALUES(?,?,?)
    """,(batch_name,timing,course_name))

    conn.commit()

    add_log(f"Batch Created : {batch_name}")

    conn.close()


def get_batches():

    conn=get_connection()

    cursor=conn.cursor()

    cursor.execute("""
    SELECT * FROM batches
    ORDER BY batch_name
    """)

    rows=cursor.fetchall()

    conn.close()

    return rows

def assign_batch(student_id, batch):

    conn=get_connection()

    cursor=conn.cursor()

    cursor.execute("""

    UPDATE students
    SET batch=?
    WHERE student_id=?

    """,(batch,student_id))

    conn.commit()

    add_log(f"Batch Assigned : Student {student_id}")

    conn.close()


def students_by_course(course):

    conn=get_connection()

    cursor=conn.cursor()

    cursor.execute("""

    SELECT student_id,
           full_name,
           mobile,
           batch

    FROM students

    WHERE course=?

    ORDER BY full_name

    """,(course,))

    rows=cursor.fetchall()

    conn.close()

    return rows

from datetime import datetime


def pay_fee(student_id, amount):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT fee_paid, course_fee
    FROM students
    WHERE student_id=?
    """, (student_id,))

    student = cursor.fetchone()

    if not student:
        conn.close()
        return False

    if amount <= 0:
        conn.close()
        return False

    new_paid = student["fee_paid"] + amount
    if new_paid > student["course_fee"]:
        conn.close()
        return False
    balance = student["course_fee"] - new_paid

    cursor.execute("""
    UPDATE students
    SET fee_paid=?, balance_fee=?
    WHERE student_id=?
    """, (new_paid, balance, student_id))

    cursor.execute("""
    INSERT INTO fee_payments(
        student_id,
        payment_date,
        amount
    )
    VALUES(?,?,?)
    """, (
        student_id,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        amount
    ))

    conn.commit()

    add_log(f"Fee Collected : Student {student_id} Amount {amount}")

    conn.close()

    return True


def payment_history(student_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM fee_payments
    WHERE student_id=?
    ORDER BY payment_date DESC
    """, (student_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


from datetime import date


def mark_attendance(student_id, status):

    conn = get_connection()
    cursor = conn.cursor()

    today = str(date.today())

    cursor.execute("SELECT 1 FROM students WHERE student_id=?", (student_id,))
    if cursor.fetchone() is None:
        conn.close()
        return False

    cursor.execute("""
    SELECT *
    FROM attendance
    WHERE student_id=? AND date=?
    """, (student_id, today))

    if cursor.fetchone():
        conn.close()
        return False

    cursor.execute("""
    INSERT INTO attendance(
        student_id,
        date,
        status
    )
    VALUES(?,?,?)
    """, (
        student_id,
        today,
        status
    ))

    conn.commit()

    add_log(f"Attendance : Student {student_id} {status}")

    conn.close()

    return True


def get_attendance(student_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM attendance
    WHERE student_id=?
    ORDER BY date DESC
    """, (student_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def attendance_percentage(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM attendance
    WHERE student_id=?
    """, (student_id,))

    total = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM attendance
    WHERE student_id=? AND status='Present'
    """, (student_id,))

    present = cursor.fetchone()[0]

    conn.close()

    if total == 0:
        return 0

    return round((present / total) * 100, 2)


def monthly_attendance(student_id, month):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM attendance
    WHERE student_id=?
    AND strftime('%m', date)=?
    ORDER BY date
    """, (student_id, month))

    rows = cursor.fetchall()

    conn.close()

    return rows

def dashboard_statistics():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM courses")
    courses = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM batches")
    batches = cursor.fetchone()[0]

    cursor.execute("SELECT IFNULL(SUM(fee_paid),0) FROM students")
    fees = cursor.fetchone()[0]

    conn.close()

    return students, courses, batches, fees

def student_report():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT student_id,
           full_name,
           course,
           batch,
           mobile
    FROM students
    ORDER BY full_name
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def fee_report():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

    student_id,

    full_name,

    course_fee,

    fee_paid,

    balance_fee

    FROM students

    ORDER BY full_name

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def attendance_report():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

    students.student_id,

    students.full_name,

    attendance.date,

    attendance.status

    FROM students

    INNER JOIN attendance

    ON students.student_id=attendance.student_id

    ORDER BY attendance.date DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def get_logs():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM logs

    ORDER BY log_id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows
