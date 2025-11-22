from typing import List, Optional
from ...domain.entities.lesson import Lesson


class LessonDTO:
    """Data Transfer Object for Lesson"""

    @staticmethod
    def from_entity(lesson: Lesson) -> dict:
        """Convert Lesson entity to DTO dictionary"""
        return lesson.to_dict()

    @staticmethod
    def from_entities(lessons: List[Lesson]) -> List[dict]:
        """Convert list of Lesson entities to list of DTO dictionaries"""
        return [LessonDTO.from_entity(lesson) for lesson in lessons]