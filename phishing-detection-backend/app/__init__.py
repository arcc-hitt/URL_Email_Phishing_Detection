from flask import Flask
from flask_cors import CORS
from config import config
from pymongo import MongoClient
from routes import url_analysis, email_analysis

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config)

    # Database setup
    mongodb_uri = app.config['MONGODB_URI']
    client = MongoClient(mongodb_uri)
    db = client["phishing_detection_db"]
    logs_collection = db['phishing_logs']

    # Import and register blueprints
    from .main import bp as logs_bp
    app.register_blueprint(logs_bp)
    app.register_blueprint(email_analysis.bp, url_prefix="/api/email")
    app.register_blueprint(url_analysis.bp, url_prefix="/api/url")

    return app

# Expose the app variable at the module level
app = create_app()
