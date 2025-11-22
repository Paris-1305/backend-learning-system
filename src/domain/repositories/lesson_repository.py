from abc import ABC, abstractmethod
from typing import List
from ..entities.lesson import Lesson


class LessonRepository(ABC):
    """Abstract repository interface for Lesson entities"""

    @abstractmethod
    def get_by_course_id(self, course_id: int) -> List[Lesson]:
        """Retrieve all lessons for a specific course"""
        pass