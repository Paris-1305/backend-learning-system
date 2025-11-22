# backend/src/domain/course.py

class Course:
    def __init__(self, id, title, description=None, category=None, image_url=None, difficulty=None):
        self.id = id
        self.title = title
        self.description = description or {"intro": "", "scope": []}  # matches TS interface
        self.category = category
        self.image_url = image_url
        self.difficulty = difficulty  # 'beginner' | 'intermediate' | 'advanced'

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "imageUrl": self.image_url,
            "difficulty": self.difficulty,
        }
