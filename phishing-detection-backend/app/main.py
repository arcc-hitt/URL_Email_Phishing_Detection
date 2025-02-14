import datetime
from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient, errors
from app.config import config
from app.routes import url_analysis, email_analysis
import os

def create_app():
    # Initialize the Flask app
    app = Flask(__name__)

    # Configure CORS globally
    CORS(
        app,
        resources={r"/*": {"origins": ["http://localhost:4200", "https://url-email-phishing-detection.vercel.app"]}},
        methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
        allow_headers=["Content-Type"]
    )

    app.config.from_object(config)
    mongodb_uri = app.config['MONGODB_URI']
    
    try:
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        client.server_info()  # Trigger exception if cannot connect to DB
    except errors.ServerSelectionTimeoutError as err:
        print(f"Failed to connect to MongoDB: {err}")
        raise

    db = client["phishing_detection_db"]
    logs_collection = db['phishing_logs']
    bp = Blueprint('logs_api', __name__)

    # Error handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({"error": str(e)}), 500

    # Route for saving phishing logs
    @bp.route('/api/phishing_logs', methods=['POST', 'OPTIONS'])
    def save_log():
        if request.method == "OPTIONS":
            return cors_preflight_response()

        try:
            log_data = request.json
            log_data['created_at'] = datetime.datetime.now()  # Add timestamp
            logs_collection.insert_one(log_data)
            response = jsonify({"message": "Log saved successfully"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 201
        except Exception as e:
            response = jsonify({"error": "Failed to save log: " + str(e)})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 500

    # Route for retrieving phishing logs
    @bp.route('/api/phishing_logs', methods=['GET'])
    def get_logs():
        try:
            logs = list(logs_collection.find())
            for log in logs:
                log["_id"] = str(log["_id"])
            response = jsonify(logs)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 200
        except Exception as e:
            response = jsonify({"error": "Failed to retrieve logs: " + str(e)})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response, 500

    # Utility for CORS preflight response
    def cors_preflight_response():
        response = jsonify({"message": "CORS preflight successful"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response, 200

    # Register blueprints for different routes
    app.register_blueprint(email_analysis.bp, url_prefix="/api/email")
    app.register_blueprint(url_analysis.bp, url_prefix="/api/url")
    app.register_blueprint(bp)

    return app

# Start the app
if __name__ == "__main__":
    if os.fork() == 0:
        app = create_app()
        app.run(host="0.0.0.0", port=5000)
