# backend/src/domain/lesson.py

class Lesson:
    def __init__(self, id, title, content=None, difficulty=None, course_id=None, image_url=None, description=None):
        self.id = id
        self.title = title
        self.content = content
        self.difficulty = difficulty  # 'easy' | 'medium' | 'hard'
        self.course_id = course_id
        self.image_url = image_url
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "difficulty": self.difficulty,
            "courseId": self.course_id,
            "imageUrl": self.image_url,
            "description": self.description,
        }
