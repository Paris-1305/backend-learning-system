# # src/config/config.py
# import os
# from dotenv import load_dotenv

# load_dotenv()  # load variables from .env

# class Config:
#     DATABASE_PATH = os.getenv("DATABASE_PATH", "backend.db")
#     VALID_API_KEYS = {os.getenv("API_KEY")}

# src/config/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # src/config
    DATABASE_PATH = os.path.join(BASE_DIR, os.getenv("DATABASE_PATH", "../../learnify.db"))
    VALID_API_KEYS = {os.getenv("API_KEY")}
