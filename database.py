import sqlite3

# Jadvalni yaratish yoki qayta yaratish funksiyasi
def create_or_recreate_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price TEXT NOT NULL,
        day TEXT,
        date TEXT,
        description TEXT NOT NULL,
        teacher_info TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Ma'lumot qo'shish funksiyasi
def insert_row_employee(name, price, day, date, description, teacher_info):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO courses (name, price, day, date, description, teacher_info)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, price, day, date, description, teacher_info))
    conn.commit()
    conn.close()

# Ma'lumotlarni o'qish funksiyasi
def fetch_all_courses():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, price, day, date, description, teacher_info FROM courses")
    courses = cursor.fetchall()
    conn.close()
    return courses
