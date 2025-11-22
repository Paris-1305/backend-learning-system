from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CourseDescription:
    """Value object for course description"""
    intro: str
    scope: List[str]


@dataclass
class Course:
    """Course entity representing a learning course"""
    
    id: int
    title: str
    description: CourseDescription
    difficulty: str
    category: Optional[str] = None
    image_url: Optional[str] = None
    lesson_count: Optional[int] = None
    duration: Optional[str] = None
    
    def __post_init__(self):
        """Validate course data"""
        if self.difficulty not in ['beginner', 'intermediate', 'advanced']:
            raise ValueError(f"Invalid difficulty level: {self.difficulty}")
        
        if not self.title or not self.title.strip():
            raise ValueError("Course title cannot be empty")
    
    def to_dict(self) -> dict:
        """Convert course to dictionary representation"""
        return {
            'id': self.id,
            'title': self.title,
            'description': {
                'intro': self.description.intro,
                'scope': self.description.scope
            },
            'category': self.category,
            'imageUrl': self.image_url,
            'difficulty': self.difficulty,
            'lessonCount': self.lesson_count,
            'duration': self.duration
        }