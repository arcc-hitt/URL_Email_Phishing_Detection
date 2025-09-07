import datetime
from flask import Blueprint, jsonify, request
from app import db

logs_collection = db['phishing_logs']
bp = Blueprint('logs_api', __name__)

# Root endpoint
@bp.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Phishing Detection Backend is running",
        "endpoints": ["/api/email", "/api/url", "/api/phishing_logs", "/health"]
    })

# Save phishing log
@bp.route('/api/phishing_logs', methods=['POST', 'OPTIONS'])
def save_log():
    if request.method == "OPTIONS":
        return cors_preflight_response()

    try:
        log_data = request.json
        log_data['created_at'] = datetime.datetime.now()
        logs_collection.insert_one(log_data)
        return jsonify({"message": "Log saved successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to save log: {e}"}), 500

# Retrieve phishing logs
@bp.route('/api/phishing_logs', methods=['GET'])
def get_logs():
    try:
        logs = list(logs_collection.find())
        for log in logs:
            log["_id"] = str(log["_id"])
        return jsonify(logs), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve logs: {e}"}), 500

# Health check
@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Phishing Detection API is running"}), 200

# Utility: CORS preflight
def cors_preflight_response():
    response = jsonify({"message": "CORS preflight successful"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS, GET")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response, 200
