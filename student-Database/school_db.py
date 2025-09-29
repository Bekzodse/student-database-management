import sqlite3
import csv

conn = sqlite3.connect("school.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    group_name TEXT NOT NULL,
    age INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    subject TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject_id INTEGER,
    grade REAL,
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(subject_id) REFERENCES subjects(id)
)
""")
conn.commit()



def add_student(name, group_name, age):
    cursor.execute("INSERT INTO students (name, group_name, age) VALUES (?, ?, ?)",
                   (name, group_name, age))
    conn.commit()
    print(f"✅ Student {name} added successfully!")

def update_student(student_id, new_name, new_group, new_age):
    cursor.execute("UPDATE students SET name=?, group_name=?, age=? WHERE id=?",
                   (new_name, new_group, new_age, student_id))
    conn.commit()
    print(f"✏️ Student ID {student_id} updated!")

def delete_student(student_id):
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    print(f"🗑️ Student ID {student_id} deleted!")

def show_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    print("\n📋 Student List:")
    for s in students:
        print(f"ID: {s[0]}, Name: {s[1]}, Group: {s[2]}, Age: {s[3]}")

def search_student(name):
    cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + name + '%',))
    results = cursor.fetchall()
    print(f"\n🔎 Search results for '{name}':")
    if results:
        for s in results:
            print(f"ID: {s[0]}, Name: {s[1]}, Group: {s[2]}, Age: {s[3]}")
    else:
        print("No student found!")


def add_teacher(name, subject):
    cursor.execute("INSERT INTO teachers (name, subject) VALUES (?, ?)", (name, subject))
    conn.commit()
    print(f"👨‍🏫 Teacher {name} ({subject}) added!")

def show_teachers():
    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()
    print("\n👨‍🏫 Teachers:")
    for t in teachers:
        print(f"ID: {t[0]}, Name: {t[1]}, Subject: {t[2]}")



def add_subject(name):
    try:
        cursor.execute("INSERT INTO subjects (name) VALUES (?)", (name,))
        conn.commit()
        print(f"📘 Subject '{name}' added!")
    except sqlite3.IntegrityError:
        print(f"⚠️ Subject '{name}' already exists!")

def show_subjects():
    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()
    print("\n📘 Subjects:")
    for sub in subjects:
        print(f"ID: {sub[0]}, Subject: {sub[1]}")



def add_grade(student_id, subject_id, grade):
    cursor.execute("INSERT INTO grades (student_id, subject_id, grade) VALUES (?, ?, ?)",
                   (student_id, subject_id, grade))
    conn.commit()
    print(f"📊 Grade added (Student {student_id}, Subject {subject_id}, Grade {grade})")

def student_grades(student_id):
    cursor.execute("""
    SELECT subjects.name, grades.grade
    FROM grades
    JOIN subjects ON grades.subject_id = subjects.id
    WHERE grades.student_id = ?
    """, (student_id,))
    results = cursor.fetchall()
    if results:
        print(f"\n📊 Grades for Student ID {student_id}:")
        for r in results:
            print(f"{r[0]}: {r[1]}")
    else:
        print("⚠️ No grades for this student.")

def best_student_in_subject(subject_id):
    cursor.execute("""
    SELECT students.name, MAX(grades.grade)
    FROM grades
    JOIN students ON grades.student_id = students.id
    WHERE grades.subject_id = ?
    """, (subject_id,))
    result = cursor.fetchone()
    if result and result[0]:
        print(f"\n🏆 Best student in Subject {subject_id}: {result[0]} with Grade {result[1]}")
    else:
        print("⚠️ No grades for this subject yet.")

def average_grade(student_id):
    cursor.execute("SELECT AVG(grade) FROM grades WHERE student_id = ?", (student_id,))
    avg = cursor.fetchone()[0]
    if avg:
        print(f"📊 Average grade for Student ID {student_id}: {round(avg, 2)}")
    else:
        print("⚠️ No grades available.")



def export_students_csv(filename="students.csv"):
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Group", "Age"])
        writer.writerows(students)
    print(f"📂 Students exported to {filename}")



# Menu System

def menu():
    while True:
        print("\n===== School Management System =====")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. Show All Students")
        print("5. Search Student by Name")
        print("6. Add Teacher")
        print("7. Show All Teachers")
        print("8. Add Subject")
        print("9. Show Subjects")
        print("10. Add Grade")
        print("11. Show Student Grades")
        print("12. Best Student in Subject")
        print("13. Student Average Grade")
        print("14. Export Students to CSV")
        print("0. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            name = input("Name: ")
            group = input("Group: ")
            age = int(input("Age: "))
            add_student(name, group, age)

        elif choice == "2":
            sid = int(input("Student ID: "))
            new_name = input("New Name: ")
            new_group = input("New Group: ")
            new_age = int(input("New Age: "))
            update_student(sid, new_name, new_group, new_age)

        elif choice == "3":
            sid = int(input("Student ID to delete: "))
            delete_student(sid)

        elif choice == "4":
            show_students()

        elif choice == "5":
            name = input("Enter student name to search: ")
            search_student(name)

        elif choice == "6":
            name = input("Teacher Name: ")
            subject = input("Subject: ")
            add_teacher(name, subject)

        elif choice == "7":
            show_teachers()

        elif choice == "8":
            sub = input("Subject name: ")
            add_subject(sub)

        elif choice == "9":
            show_subjects()

        elif choice == "10":
            sid = int(input("Student ID: "))
            subid = int(input("Subject ID: "))
            grade = float(input("Grade: "))
            add_grade(sid, subid, grade)

        elif choice == "11":
            sid = int(input("Student ID: "))
            student_grades(sid)

        elif choice == "12":
            subid = int(input("Subject ID: "))
            best_student_in_subject(subid)

        elif choice == "13":
            sid = int(input("Student ID: "))
            average_grade(sid)

        elif choice == "14":
            export_students_csv()

        elif choice == "0":
            print("📌 Exiting program...")
            break
        else:
            print("❌ Invalid choice!")


menu()
conn.close()
