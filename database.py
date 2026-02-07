import sqlite3
import os
from config import DB_FILE, DATA_DIR, STUDENT_IMAGES_DIR, GROUP_PHOTOS_DIR, DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database, creates tables, and seeds default data."""
    # Ensure data directories exist
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(STUDENT_IMAGES_DIR, exist_ok=True)
    os.makedirs(GROUP_PHOTOS_DIR, exist_ok=True)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS Teachers (
            teacher_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            branch TEXT,
            subject TEXT NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS Students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            roll TEXT NOT NULL,
            section TEXT NOT NULL,
            class TEXT NOT NULL,
            password TEXT NOT NULL,
            photo_path TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS Attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            subject TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            marked_by TEXT NOT NULL,
            UNIQUE(student_id, subject, date),
            FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE,
            FOREIGN KEY (marked_by) REFERENCES Teachers(teacher_id)
        );
        CREATE TABLE IF NOT EXISTS Meta (
            key TEXT PRIMARY KEY,
            value INTEGER NOT NULL
        );
    """)

    # Seed default admin if not exists
    cursor.execute("SELECT * FROM Admins WHERE email = ?", (DEFAULT_ADMIN_EMAIL,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO Admins (email, password) VALUES (?, ?)", (DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD))

    # Seed meta counters if not exists
    cursor.execute("INSERT OR IGNORE INTO Meta (key, value) VALUES ('last_teacher_serial', 0);")
    cursor.execute("INSERT OR IGNORE INTO Meta (key, value) VALUES ('last_student_serial', 0);")

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

# --- Meta Table Functions ---
def get_next_serial(key):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM Meta WHERE key = ?", (key,))
    current_value = cursor.fetchone()['value']
    new_value = current_value + 1
    cursor.execute("UPDATE Meta SET value = ? WHERE key = ?", (new_value, key))
    conn.commit()
    conn.close()
    return new_value

# --- User Creation ---
def create_teacher(teacher_id, name, email, branch, subject, password):
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO Teachers (teacher_id, name, email, branch, subject, password) VALUES (?, ?, ?, ?, ?, ?)",
            (teacher_id, name, email, branch, subject, password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def create_student(student_id, name, roll, section, _class, password, photo_path):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO Students (student_id, name, roll, section, class, password, photo_path) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (student_id, name, roll, section, _class, password, photo_path)
    )
    conn.commit()
    conn.close()
    return True

# --- Data Retrieval ---
def get_admin_by_email(email):
    conn = get_db_connection()
    admin = conn.execute("SELECT * FROM Admins WHERE email = ?", (email,)).fetchone()
    conn.close()
    return admin

def get_teacher(teacher_id):
    conn = get_db_connection()
    teacher = conn.execute("SELECT * FROM Teachers WHERE teacher_id = ?", (teacher_id,)).fetchone()
    conn.close()
    return teacher

def get_student(student_id):
    conn = get_db_connection()
    student = conn.execute("SELECT * FROM Students WHERE student_id = ?", (student_id,)).fetchone()
    conn.close()
    return student

def list_teachers():
    conn = get_db_connection()
    teachers = conn.execute("SELECT teacher_id, name, email, branch, subject FROM Teachers").fetchall()
    conn.close()
    return teachers

def list_students():
    conn = get_db_connection()
    students = conn.execute("SELECT student_id, name, roll, section, class FROM Students").fetchall()
    conn.close()
    return students

# --- Attendance Functions ---
def mark_attendance(student_id, subject, date_iso, status, marked_by):
    conn = get_db_connection()
    conn.execute(
        """
        INSERT INTO Attendance (student_id, subject, date, status, marked_by) VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(student_id, subject, date) DO UPDATE SET status = excluded.status, marked_by = excluded.marked_by
        """,
        (student_id, subject, date_iso, status, marked_by)
    )
    conn.commit()
    conn.close()

def get_attendance_by_student(student_id):
    conn = get_db_connection()
    records = conn.execute(
        "SELECT date, subject, status FROM Attendance WHERE student_id = ? ORDER BY date DESC", (student_id,)
    ).fetchall()
    conn.close()
    return records

# --- YEH NAYE FUNCTIONS HAIN ---
# --- User Deletion Functions ---
def delete_teacher(teacher_id):
    """Deletes a teacher record from the database."""
    conn = get_db_connection()
    conn.execute("DELETE FROM Teachers WHERE teacher_id = ?", (teacher_id,))
    conn.commit()
    conn.close()

def delete_student(student_id):
    """Deletes a student record, their attendance, and their photo file."""
    conn = get_db_connection()
    
    # Pehle student ki photo ka path get karein
    student = conn.execute("SELECT photo_path FROM Students WHERE student_id = ?", (student_id,)).fetchone()
    
    # Database se student record delete karein
    conn.execute("DELETE FROM Students WHERE student_id = ?", (student_id,))
    
    # Student ke saare attendance records bhi delete kar dein
    conn.execute("DELETE FROM Attendance WHERE student_id = ?", (student_id,))
    
    conn.commit()
    conn.close()
    
    # Agar photo hai, to use folder se bhi delete karein
    if student and student['photo_path'] and os.path.exists(student['photo_path']):
        try:
            os.remove(student['photo_path'])
        except OSError as e:
            print(f"Error deleting photo file {student['photo_path']}: {e}")