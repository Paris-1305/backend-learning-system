from typing import Optional
from ...domain.repositories.course_repository import CourseRepository
from ..dto.course_dto import CourseDTO


class GetCourseById:
    """Use case for retrieving a course by ID"""

    def __init__(self, course_repository: CourseRepository):
        self.course_repository = course_repository

    def execute(self, course_id: int) -> Optional[dict]:
        """Execute the use case"""
        course = self.course_repository.get_by_id(course_id)
        if course is None:
            return None
        return CourseDTO.from_entity(course)
