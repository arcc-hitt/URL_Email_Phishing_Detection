import datetime
from flask import Blueprint, jsonify, request
from pymongo import errors
from app import app, db

logs_collection = db['phishing_logs']
bp = Blueprint('logs_api', __name__)

# Error handler
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500

# Root endpoint
@bp.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Phishing Detection Backend is running",
        "endpoints": ["/api/email", "/api/url", "/api/phishing_logs", "/health"]
    })

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

# Health check endpoint
@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Phishing Detection API is running"}), 200

# Utility for CORS preflight response
def cors_preflight_response():
    response = jsonify({"message": "CORS preflight successful"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS, GET")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response, 200

# Start the app
# if __name__ == "__main__":
#     from .config import config
#     app.run(host="0.0.0.0", port=config.PORT)