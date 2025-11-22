# src/config.py
import os

class Config:
    DATABASE_PATH = "backend.db"
    VALID_API_KEYS = { os.environ.get("API_KEY") }

