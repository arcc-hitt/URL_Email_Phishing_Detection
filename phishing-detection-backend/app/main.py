import datetime
from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from .config import config
from .routes import url_analysis, email_analysis
from pymongo import MongoClient

def create_app():
    # Initialize the Flask app
    app = Flask(__name__)
    # Configure CORS with specific settings
    CORS(app)
    app.config.from_object(config)
    mongodb_uri = app.config['MONGODB_URI']
    client = MongoClient(mongodb_uri)
    db = client["phishing_detection_db"]
    logs_collection = db['phishing_logs']
    bp = Blueprint('logs_api', __name__)
    
    @bp.route('/api/phishing_logs', methods=['POST'])
    def save_log():
        log_data = request.json
        log_data['created_at'] = datetime.datetime.now()  # Add timestamp
        logs_collection.insert_one(log_data)
        response = jsonify({"message": "Log saved successfully"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 201
    
    @bp.route('/api/phishing_logs', methods=['GET'])
    def get_logs():
        logs = list(logs_collection.find())
        for log in logs:
            log["_id"] = str(log["_id"])
        return jsonify(logs), 200

    # Register blueprints for different routes
    app.register_blueprint(email_analysis.bp, url_prefix="/api/email")
    app.register_blueprint(url_analysis.bp, url_prefix="/api/url")
    app.register_blueprint(bp)

    return app

# Start the app
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)