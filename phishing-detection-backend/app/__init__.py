from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from .config import config

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
        ]
    }
})


# Initialize MongoDB client
mongodb_uri = app.config['MONGODB_URI']
if not mongodb_uri:
    raise ValueError("MONGODB_URI environment variable is not set")

client = MongoClient(mongodb_uri)
db = client["phishing_detection_db"]

# Test MongoDB connection
try:
    client.admin.command('ismaster')
    print("MongoDB connection successful")
except Exception as e:
    print(f"MongoDB connection failed: {e}")

# Register blueprints
from .routes import url_analysis, email_analysis
from .main import bp as logs_bp

app.register_blueprint(email_analysis.bp, url_prefix="/api/email")
app.register_blueprint(url_analysis.bp, url_prefix="/api/url")
app.register_blueprint(logs_bp)
