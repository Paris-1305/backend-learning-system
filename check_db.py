import sqlite3
from config import Config

def check_database():
    print("🔍 Checking SQLite database...")
    print(f"📌 Database path: {Config.DATABASE_PATH}")

    try:
        conn = sqlite3.connect(Config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Check table existence
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("\n📌 Tables in DB:")
        for t in tables:
            print(" -", t["name"])

        # Count courses
        cursor.execute("SELECT COUNT(*) as count FROM courses")
        course_count = cursor.fetchone()["count"]
        print(f"\n📘 Courses count: {course_count}")

        # Count lessons
        cursor.execute("SELECT COUNT(*) as count FROM lessons")
        lesson_count = cursor.fetchone()["count"]
        print(f"📗 Lessons count: {lesson_count}")

        # Show all course titles
        cursor.execute("SELECT id, title FROM courses")
        courses = cursor.fetchall()

        print("\n📚 Courses:")
        for c in courses:
            print(f" - ({c['id']}) {c['title']}")

        conn.close()

    except Exception as e:
        print("❌ ERROR:", str(e))

if __name__ == "__main__":
    check_database()
