# import sqlite3
# import json
# from typing import List, Optional
# from src.domain.entities.course import Course, CourseDescription
# from src.domain.repositories.course_repository import CourseRepository
# from src.infrastructure.database.connection import DatabaseConnection


# class SQLiteCourseRepository(CourseRepository):
#     """SQLite implementation of CourseRepository"""

#     def __init__(self):
#         self.db = DatabaseConnection()
#         self._ensure_sample_data()

#     def _get_connection(self):
#         """Return a connection with dictionary row access"""
#         conn = self.db.get_connection()
#         conn.row_factory = sqlite3.Row
#         return conn

#     def get_all(self) -> List[Course]:
#         """Retrieve all courses from database"""
#         conn = self._get_connection()
#         cursor = conn.cursor()

#         cursor.execute('SELECT * FROM courses ORDER BY id')
#         rows = cursor.fetchall()
#         conn.close()

#         return [self._row_to_entity(row) for row in rows]

#     def get_by_id(self, course_id: int) -> Optional[Course]:
#         """Retrieve a course by its ID"""
#         conn = self._get_connection()
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
#         row = cursor.fetchone()
#         conn.close()
#         return self._row_to_entity(row) if row else None

#     def _row_to_entity(self, row) -> Course:
#         """Convert database row to Course entity"""
#         description_scope = json.loads(row['description_scope']) if row['description_scope'] else []
#         description = CourseDescription(
#             intro=row['description_intro'],
#             scope=description_scope
#         )
#         return Course(
#             id=row['id'],
#             title=row['title'],
#             description=description,
#             difficulty=row['difficulty'],
#             category=row['category'],
#             image_url=row['image_url'],
#             lesson_count=row['lesson_count'] or 0,
#             duration=row['duration'] or 0
#         )

#     def create(self, data: dict) -> Course:
#         conn = self._get_connection()
#         cursor = conn.cursor()
#         cursor.execute(
#             "INSERT INTO courses (title, description_intro, description_scope, category, image_url, difficulty, lesson_count, duration) "
#             "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
#             (
#                 data.get("title"),
#                 data.get("description_intro"),
#                 json.dumps(data.get("description_scope", [])),
#                 data.get("category"),
#                 data.get("image_url"),
#                 data.get("difficulty"),
#                 data.get("lesson_count", 0),
#                 data.get("duration", 0),
#             )
#         )
#         conn.commit()
#         course_id = cursor.lastrowid
#         conn.close()
#         return self.get_by_id(course_id)

#     def update(self, course_id: int, data: dict) -> Optional[Course]:
#         conn = self._get_connection()
#         cursor = conn.cursor()
#         cursor.execute(
#             "UPDATE courses SET title=?, description_intro=?, description_scope=?, category=?, image_url=?, difficulty=?, lesson_count=?, duration=? WHERE id=?",
#             (
#                 data.get("title"),
#                 data.get("description_intro"),
#                 json.dumps(data.get("description_scope", [])),
#                 data.get("category"),
#                 data.get("image_url"),
#                 data.get("difficulty"),
#                 data.get("lesson_count", 0),
#                 data.get("duration", 0),
#                 course_id
#             )
#         )
#         conn.commit()
#         conn.close()
#         return self.get_by_id(course_id)

#     def delete(self, course_id: int) -> bool:
#         conn = self._get_connection()
#         cursor = conn.cursor()
#         cursor.execute("DELETE FROM courses WHERE id=?", (course_id,))
#         conn.commit()
#         rowcount = cursor.rowcount
#         conn.close()
#         return rowcount > 0

# #     def _ensure_sample_data(self):
# #         """Insert sample courses if none exist"""
# #         if len(self.get_all()) == 0:
# #             print("No courses found. Inserting sample data...")
# #             sample_courses = [
# #        {
# #         "title": "Python Basics",
# #         "description_intro": "Learn Python from scratch",
# #         "description_scope": ["variables", "loops", "functions"],
# #         "category": "Programming",
# #         "image_url": "https://example.com/python.png",
# #         "difficulty": "beginner",  # ✅ must be exactly one of the allowed values
# #         "lesson_count": 10,
# #         "duration": 120
# #     },
# #     {
# #         "title": "Advanced Python",
# #         "description_intro": "Deep dive into Python",
# #         "description_scope": ["decorators", "generators", "asyncio"],
# #         "category": "Programming",
# #         "image_url": "https://example.com/adv-python.png",
# #         "difficulty": "advanced",  # ✅ correct spelling
# #         "lesson_count": 15,
# #         "duration": 180
# #     }
# # ]
# #             for course in sample_courses:
# #   self.create(course)

import sqlite3
import json
from typing import List, Optional
from src.domain.entities.course import Course, CourseDescription
from src.domain.repositories.course_repository import CourseRepository
from src.infrastructure.database.connection import DatabaseConnection


class SQLiteCourseRepository(CourseRepository):

    def __init__(self):
        self.db = DatabaseConnection()

    def _get_connection(self):
        """Get connection with dictionary access"""
        return self.db.get_connection()

    def get_all(self) -> List[Course]:
      conn = self._get_connection()
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM courses ORDER BY id")  # ordering by id
      rows = cursor.fetchall()
      conn.close()
      return [self._row_to_entity(row) for row in rows]


    def get_by_id(self, course_id: int) -> Optional[Course]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses WHERE id=?", (course_id,))
        row = cursor.fetchone()
        conn.close()
        return self._row_to_entity(row) if row else None

    def _row_to_entity(self, row) -> Course:
        description_scope = json.loads(row["description_scope"]) if row["description_scope"] else []
        description = CourseDescription(
            intro=row["description_intro"],
            scope=description_scope
        )
        return Course(
            id=row["id"],
            title=row["title"],
            description=description,
            difficulty=row["difficulty"],
            category=row["category"],
            image_url=row["image_url"],
            lesson_count=row["lesson_count"] or 0,
            duration=row["duration"] or 0
        )

    def create(self, data: dict) -> Course:
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO courses (title, description_intro, description_scope, category, image_url, difficulty, lesson_count, duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("title"),
            data.get("description_intro"),
            json.dumps(data.get("description_scope", [])),
            data.get("category"),
            data.get("image_url"),
            data.get("difficulty"),
            data.get("lesson_count", 0),
            data.get("duration", 0),
        ))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return self.get_by_id(new_id)

    def update(self, course_id: int, data: dict) -> Optional[Course]:
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE courses
            SET title=?, description_intro=?, description_scope=?, category=?, image_url=?, difficulty=?, lesson_count=?, duration=?
            WHERE id=?
        """, (
            data.get("title"),
            data.get("description_intro"),
            json.dumps(data.get("description_scope", [])),
            data.get("category"),
            data.get("image_url"),
            data.get("difficulty"),
            data.get("lesson_count", 0),
            data.get("duration", 0),
            course_id
        ))

        conn.commit()
        conn.close()

        return self.get_by_id(course_id)

    def delete(self, course_id: int) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM courses WHERE id=?", (course_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted
