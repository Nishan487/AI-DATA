import mysql.connector
from mysql.connector import Error

def assign_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nishan@20640904"
    )

    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS grade_db")
    cursor.execute("USE grade_db")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            subject VARCHAR(255) NOT NULL,
            score FLOAT NOT NULL,
            grade TEXT
        )
    """)

    students_data = [
        ('Alice', 'Math', 85),
        ('Bob', 'Math', 78),
        ('Charlie', 'Math', 92),
        ('David', 'Math', 65),
        ('Eve', 'Math', 45),
        ('Frank', 'Science', 90),
        ('Grace', 'Science', 82),
        ('Henry', 'Science', 88),
        ('Ivy', 'Science', 70),
        ('Jack', 'Science', 48),
        ('Kevin', 'History', 78),
        ('Lily', 'History', 85),
        ('Mason', 'History', 80),
        ('Nora', 'History', 72),
        ('Olivia', 'History', 60)
    ]

    for student in students_data:
        cursor.execute(
            "SELECT * FROM students WHERE name=%s AND subject=%s",
            (student[0], student[1])
        )

        existing_student = cursor.fetchone()

        if existing_student:
            print(f"Student {student[0]} already exists. Skipping insertion.")
        else:
            grade = assign_grade(student[2])

            cursor.execute("""
                INSERT INTO students (name, subject, score, grade)
                VALUES (%s, %s, %s, %s)
            """, (student[0], student[1], student[2], grade))

    conn.commit()

    cursor.execute("SELECT id, score FROM students")

    rows = cursor.fetchall()

    for row in rows:
        student_id = row[0]
        score = row[1]
        grade = assign_grade(score)

        cursor.execute("""
            UPDATE students
            SET grade=%s
            WHERE id=%s
        """, (grade, student_id))

    conn.commit()

    cursor.execute("DELETE FROM students WHERE score < 50")
    conn.commit()

    cursor.execute("SHOW COLUMNS FROM students LIKE 'passed'")
    column_exists = cursor.fetchone()

    if not column_exists:
        cursor.execute("""
            ALTER TABLE students
            ADD passed BOOLEAN
        """)

    cursor.execute("""
        UPDATE students
        SET passed = CASE
            WHEN score >= 50 THEN TRUE
            ELSE FALSE
        END
    """)

    conn.commit()

    print("\nStudents Table:")
    print(f"{'ID':<5} {'Name':<10} {'Subject':<10} {'Score':<8} {'Grade':<8} {'Passed'}")
    print("-" * 60)

    cursor.execute("""
        SELECT id, name, subject, score, grade, passed
        FROM students
    """)

    rows = cursor.fetchall()

    for row in rows:
        print(f"{row[0]:<5} {row[1]:<10} {row[2]:<10} {row[3]:<8} {row[4]:<8} {row[5]}")

    print("\nCount of Students Per Grade:")

    cursor.execute("""
        SELECT grade, COUNT(*) AS total
        FROM students
        GROUP BY grade
        ORDER BY FIELD(grade, 'A', 'B', 'C', 'D', 'F')
    """)

    grade_rows = cursor.fetchall()

    print(f"{'Grade':<10} {'Count'}")
    print("-" * 20)

    for row in grade_rows:
        print(f"{row[0]:<10} {row[1]}")

    cursor.close()
    conn.close()

except Error as e:
    print(f"Database Error: {e}")