from typing import List
from ...domain.repositories.course_repository import CourseRepository
from ..dto.course_dto import CourseDTO


class GetAllCourses:
    """Use case for retrieving all courses"""

    def __init__(self, course_repository: CourseRepository):
        self.course_repository = course_repository

    def execute(self) -> List[dict]:
        """Execute the use case"""
        courses = self.course_repository.get_all()
        return CourseDTO.from_entities(courses)