import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class Config:
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key_change_in_production")
    
    # Debug mode
    DEBUG = os.getenv("DEBUG", "False").lower() in ['true', '1', 'yes']
    
    # Database
    MONGODB_URI = os.getenv("MONGODB_URI")
    
    # Server
    PORT = int(os.getenv("PORT", 5000))
    
    # Application settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    
    def __init__(self):
        # Validate required environment variables
        if not self.MONGODB_URI:
            logger.warning("MONGODB_URI not set - database operations will fail")
        
        if self.SECRET_KEY == "default_secret_key_change_in_production":
            logger.warning("Using default SECRET_KEY - change this in production!")

config = Config()
