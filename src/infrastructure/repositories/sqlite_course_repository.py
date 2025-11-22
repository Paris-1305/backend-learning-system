# import json
# from typing import List, Optional
# from ...domain.entities.course import Course, CourseDescription
# from ...domain.repositories.course_repository import CourseRepository
# from ..database.connection import DatabaseConnection


# class SQLiteCourseRepository(CourseRepository):
#     """SQLite implementation of CourseRepository"""
    
#     def __init__(self):
#         self.db = DatabaseConnection()
    
#     def get_all(self) -> List[Course]:
#         """Retrieve all courses from database"""
#         conn = self.db.get_connection()
#         cursor = conn.cursor()
        
#         cursor.execute('SELECT * FROM courses ORDER BY id')
#         rows = cursor.fetchall()
#         conn.close()
        
#         courses = []
#         for row in rows:
#             course = self._row_to_entity(row)
#             courses.append(course)
        
#         return courses
    
#     def get_by_id(self, course_id: int) -> Optional[Course]:
#         """Retrieve a course by its ID"""
#         conn = self.db.get_connection()
#         cursor = conn.cursor()
        
#         cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
#         row = cursor.fetchone()
#         conn.close()
        
#         if row is None:
#             return None
        
#         return self._row_to_entity(row)
    
#     def _row_to_entity(self, row) -> Course:
#         """Convert database row to Course entity"""
#         description_scope = json.loads(row['description_scope'])
        
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
#             lesson_count=row['lesson_count'],
#             duration=row['duration']
#         )
        
import json
from typing import List, Optional
from ...domain.entities.course import Course, CourseDescription
from ...domain.repositories.course_repository import CourseRepository
from ..database.connection import DatabaseConnection

class SQLiteCourseRepository(CourseRepository):
    """SQLite implementation of CourseRepository"""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def get_all(self) -> List[Course]:
        """Retrieve all courses from database"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM courses ORDER BY id')
        rows = cursor.fetchall()
        conn.close()
        
        courses = [self._row_to_entity(row) for row in rows]
        return courses
    
    def get_by_id(self, course_id: int) -> Optional[Course]:
        """Retrieve a course by its ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
        row = cursor.fetchone()
        conn.close()
        
        return self._row_to_entity(row) if row else None
    
    def _row_to_entity(self, row) -> Course:
        """Convert database row to Course entity"""
        description_scope = json.loads(row['description_scope'])
        description = CourseDescription(intro=row['description_intro'], scope=description_scope)
        return Course(
            id=row['id'],
            title=row['title'],
            description=description,
            difficulty=row['difficulty'],
            category=row['category'],
            image_url=row['image_url'],
            lesson_count=row['lesson_count'],
            duration=row['duration']
        )
    
    def create(self, data: dict) -> Course:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO courses (title, description_intro, description_scope, category, image_url, difficulty) VALUES (?, ?, ?, ?, ?, ?)",
            (
                data.get("title"),
                data.get("description_intro"),
                json.dumps(data.get("description_scope", [])),
                data.get("category"),
                data.get("image_url"),
                data.get("difficulty")
            )
        )
        conn.commit()
        course_id = cursor.lastrowid
        conn.close()
        return self.get_by_id(course_id)

    def update(self, course_id: int, data: dict) -> Optional[Course]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE courses SET title=?, description_intro=?, description_scope=?, category=?, image_url=?, difficulty=? WHERE id=?",
            (
                data.get("title"),
                data.get("description_intro"),
                json.dumps(data.get("description_scope", [])),
                data.get("category"),
                data.get("image_url"),
                data.get("difficulty"),
                course_id
            )
        )
        conn.commit()
        conn.close()
        return self.get_by_id(course_id)

    def delete(self, course_id: int) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM courses WHERE id=?", (course_id,))
        conn.commit()
        rowcount = cursor.rowcount
        conn.close()
        return rowcount > 0
