import datetime
from flask import Blueprint, jsonify, request, make_response
import traceback

from app import db

bp = Blueprint('logs_api', __name__)

# Initialize logs collection only if db is available
logs_collection = db['phishing_logs'] if db else None

# Root endpoint
@bp.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Phishing Detection Backend is running",
        "endpoints": ["/api/email/analyze", "/api/url/analyze", "/api/phishing_logs", "/health"],
        "status": "operational"
    })

# Save phishing log
@bp.route('/api/phishing_logs', methods=['POST', 'OPTIONS'])
def save_log():
    if request.method == "OPTIONS":
        return cors_preflight_response()

    try:
        if not logs_collection:
            return jsonify({"error": "Database connection not available"}), 503
            
        log_data = request.get_json(force=True)
        log_data['created_at'] = datetime.datetime.utcnow()
        logs_collection.insert_one(log_data)
        
        response = jsonify({"message": "Log saved successfully"})
        add_cors_headers(response)
        return response, 201
        
    except Exception as e:
        print(f"Error saving log: {str(e)}")
        print(traceback.format_exc())
        
        response = jsonify({"error": f"Failed to save log: {str(e)}"})
        add_cors_headers(response)
        return response, 500

# Retrieve phishing logs
@bp.route('/api/phishing_logs', methods=['GET', 'OPTIONS'])
def get_logs():
    if request.method == "OPTIONS":
        return cors_preflight_response()
        
    try:
        if not logs_collection:
            return jsonify({"error": "Database connection not available"}), 503
            
        logs = list(logs_collection.find())
        for log in logs:
            log["_id"] = str(log["_id"])
            
        response = jsonify(logs)
        add_cors_headers(response)
        return response, 200
        
    except Exception as e:
        print(f"Error retrieving logs: {str(e)}")
        print(traceback.format_exc())
        
        response = jsonify({"error": f"Failed to retrieve logs: {str(e)}"})
        add_cors_headers(response)
        return response, 500

# Health check
@bp.route('/health', methods=['GET'])
def health_check():
    db_status = "connected" if db and logs_collection else "disconnected"
    
    return jsonify({
        "status": "healthy",
        "message": "Phishing Detection API is running",
        "database": db_status,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }), 200

# Utility: CORS preflight
def cors_preflight_response():
    response = make_response()
    add_cors_headers(response)
    return response, 200

# Utility: Add CORS headers
def add_cors_headers(response):
    origin = request.headers.get("Origin")
    allowed_origins = [
        "https://url-email-phishing-detection.vercel.app",
        "http://localhost:3000",
        "http://localhost:4200"
    ]
    
    if origin in allowed_origins:
        response.headers.add("Access-Control-Allow-Origin", origin)
    else:
        response.headers.add("Access-Control-Allow-Origin", "*")
    
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, Accept")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    response.headers.add("Access-Control-Max-Age", "3600")
    
    return response

@bp.after_request
def after_request(response):
    """Ensure CORS headers are added to all responses"""
    add_cors_headers(response)
    return response