# src/config/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # load variables from .env

class Config:
    DATABASE_PATH = os.getenv("DATABASE_PATH", "backend.db")
    VALID_API_KEYS = {os.getenv("API_KEY")}


