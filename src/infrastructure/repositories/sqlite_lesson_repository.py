from typing import List, Optional
from ...domain.entities.lesson import Lesson
from ...domain.repositories.lesson_repository import LessonRepository
from ..database.connection import DatabaseConnection


class SQLiteLessonRepository(LessonRepository):
    """SQLite implementation of LessonRepository"""

    def __init__(self):
        self.db = DatabaseConnection()

    def get_by_course_id(self, course_id: int) -> List[Lesson]:
        """Retrieve all lessons for a specific course"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT * FROM lessons WHERE course_id = ? ORDER BY lesson_order',
            (course_id,)
        )
        rows = cursor.fetchall()
        conn.close()

        lessons = []
        for row in rows:
            lesson = self._row_to_entity(row)
            lessons.append(lesson)

        return lessons

    def get_all(self) -> List[Lesson]:
        """Retrieve all lessons"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM lessons ORDER BY id')
        rows = cursor.fetchall()
        conn.close()

        lessons = []
        for row in rows:
            lesson = self._row_to_entity(row)
            lessons.append(lesson)

        return lessons

    def get_by_id(self, lesson_id: int) -> Optional[Lesson]:
        """Retrieve a lesson by its ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM lessons WHERE id = ?', (lesson_id,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return self._row_to_entity(row)

    def _row_to_entity(self, row) -> Lesson:
        """Convert database row to Lesson entity"""
        return Lesson(
            id=row['id'],
            title=row['title'],
            content=row['content'],
            difficulty=row['difficulty'],
            course_id=row['course_id'],
            image_url=row['image_url'],
            description=row['description'],
            duration=row['duration'],
            lesson_order=row['lesson_order']
        )
