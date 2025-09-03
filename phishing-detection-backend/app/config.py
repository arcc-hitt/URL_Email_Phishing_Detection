import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key_change_in_production")
    DEBUG = os.getenv("DEBUG", "False").lower() in ['true', '1', 'yes']
    MONGODB_URI = os.getenv("MONGODB_URI")
    PORT = int(os.getenv("PORT", 5000))

config = Config()