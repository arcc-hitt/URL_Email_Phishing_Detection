from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Import configuration
from .config import config
app.config.from_object(config)

# Initialize MongoDB client
mongodb_uri = app.config['MONGODB_URI']
client = MongoClient(mongodb_uri)
db = client["phishing_detection_db"]

# Import and register blueprints
from .routes import url_analysis, email_analysis
app.register_blueprint(email_analysis.bp, url_prefix="/api/email")
app.register_blueprint(url_analysis.bp, url_prefix="/api/url")

# Import and register the logs blueprint
from .main import bp as logs_bp
app.register_blueprint(logs_bp)
