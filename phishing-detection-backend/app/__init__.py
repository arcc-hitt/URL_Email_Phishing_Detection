import os
import logging
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from .config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(config)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "https://url-email-phishing-detection.vercel.app",
                "http://localhost:4200",
                "http://localhost:3000"
            ],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize MongoDB client
    mongodb_uri = app.config['MONGODB_URI']
    if not mongodb_uri:
        logger.error("MONGODB_URI environment variable is not set")
        raise ValueError("MONGODB_URI environment variable is not set")
    
    try:
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        db = client["phishing_detection_db"]
        
        # Test MongoDB connection
        client.admin.command('ismaster')
        logger.info("MongoDB connection successful")
        
        # Make client and db available to the app
        app.mongodb_client = client
        app.mongodb_db = db
        
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")
        raise e
    
    # Register blueprints
    try:
        from .routes import url_analysis, email_analysis
        from .main import bp as logs_bp
        
        app.register_blueprint(email_analysis.bp, url_prefix="/api/email")
        app.register_blueprint(url_analysis.bp, url_prefix="/api/url")
        app.register_blueprint(logs_bp)
        
        logger.info("Blueprints registered successfully")
        
    except Exception as e:
        logger.error(f"Failed to register blueprints: {e}")
        raise e
    
    # Add health check endpoint
    @app.route('/health')
    def health_check():
        return {"status": "healthy", "message": "Phishing Detection API is running"}
    
    # Add error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Endpoint not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return {"error": "Internal server error"}, 500
    
    logger.info("Flask app created successfully")
    return app

# Create the app instance
app = create_app()
