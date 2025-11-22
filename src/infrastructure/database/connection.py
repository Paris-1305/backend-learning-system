import sqlite3
from typing import Optional
from config import Config


class DatabaseConnection:
    """Manages SQLite database connections"""
    
    _instance: Optional['DatabaseConnection'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.db_path = Config.DATABASE_PATH
        self._initialized = True
        self._init_database()
    
    def _init_database(self):
        """Initialize database with tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create courses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description_intro TEXT NOT NULL,
                description_scope TEXT NOT NULL,
                category TEXT,
                image_url TEXT,
                difficulty TEXT NOT NULL CHECK(difficulty IN ('beginner', 'intermediate', 'advanced')),
                lesson_count INTEGER,
                duration TEXT
            )
        ''')
        
        # Create lessons table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                difficulty TEXT NOT NULL CHECK(difficulty IN ('easy', 'medium', 'hard')),
                course_id INTEGER NOT NULL,
                image_url TEXT,
                description TEXT,
                duration INTEGER,
                lesson_order INTEGER,
                FOREIGN KEY (course_id) REFERENCES courses (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # def get_connection(self) -> sqlite3.Connection:
    #     """Get a new database connection"""
    #     conn = sqlite3.connect(self.db_path)
    #     conn.row_factory = sqlite3.Row
    #     return conn
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # ✅ allow dict-style access
        return conn