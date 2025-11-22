from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.course import Course


class CourseRepository(ABC):
    """Abstract repository interface for Course entities"""

    @abstractmethod
    def get_all(self) -> List[Course]:
        """Retrieve all courses"""
        pass

    @abstractmethod
    def get_by_id(self, course_id: int) -> Optional[Course]:
        """Retrieve a course by its ID"""
        pass