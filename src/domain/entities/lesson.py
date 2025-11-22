from dataclasses import dataclass
from typing import Optional


@dataclass
class Lesson:
    """Lesson entity representing a learning lesson"""

    id: int
    title: str
    difficulty: str
    course_id: int
    content: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    lesson_order: Optional[int] = None

    def __post_init__(self):
        """Validate lesson data"""
        if self.difficulty not in ['easy', 'medium', 'hard']:
            raise ValueError(f"Invalid difficulty level: {self.difficulty}")

        if not self.title or not self.title.strip():
            raise ValueError("Lesson title cannot be empty")

        if self.course_id <= 0:
            raise ValueError("Course ID must be positive")

    def to_dict(self) -> dict:
        """Convert lesson to dictionary representation"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'difficulty': self.difficulty,
            'courseId': self.course_id,
            'imageUrl': self.image_url,
            'description': self.description,
            'duration': self.duration,
            'lessonOrder': self.lesson_order
        } # The problematic trailing comma has been removed here.