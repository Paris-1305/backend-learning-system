from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

class Config:
    DATABASE_PATH = "backend.db"
    VALID_API_KEYS = {os.getenv("API_KEY")}
