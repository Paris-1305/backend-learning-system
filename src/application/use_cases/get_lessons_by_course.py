from typing import List
from ...domain.repositories.lesson_repository import LessonRepository
from ..dto.lesson_dto import LessonDTO


class GetLessonsByCourse:
    """Use case for retrieving lessons for a specific course"""

    def __init__(self, lesson_repository: LessonRepository):
        self.lesson_repository = lesson_repository

    def execute(self, course_id: int) -> List[dict]:
        """Execute the use case"""
        lessons = self.lesson_repository.get_by_course_id(course_id)
        return LessonDTO.from_entities(lessons)