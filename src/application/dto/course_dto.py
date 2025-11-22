from typing import List, Optional
from ...domain.entities.course import Course


class CourseDTO:
    """Data Transfer Object for Course"""
    
    @staticmethod
    def from_entity(course: Course) -> dict:
        """Convert Course entity to DTO dictionary"""
        return course.to_dict()
    
    @staticmethod
    def from_entities(courses: List[Course]) -> List[dict]:
        """Convert list of Course entities to list of DTO dictionaries"""
        return [CourseDTO.from_entity(course) for course in courses]