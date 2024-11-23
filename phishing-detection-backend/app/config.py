import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    DEBUG = os.getenv("DEBUG", True)
    MONGODB_URI = os.getenv("MONGODB_URI")

config = Config()
