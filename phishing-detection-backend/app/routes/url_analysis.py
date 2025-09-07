from flask import Blueprint, request, jsonify, make_response
from app.services.url_service import URLService
import traceback

bp = Blueprint("url_analysis", __name__)
url_service = URLService()

@bp.route("/analyze", methods=["POST", "OPTIONS"])
def analyze_url():
    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, Accept")
        response.headers.add("Access-Control-Max-Age", "3600")
        return response, 200

    try:
        # Get JSON data
        data = request.get_json(force=True)
        url = data.get("url", "")
        
        if not url:
            response = jsonify({"error": "URL is required"})
            response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
            return response, 400
        
        # Analyze the URL
        result = url_service.analyze_url(url)
        
        # Create response with CORS headers
        response = jsonify(result)
        response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
        response.headers.add("Access-Control-Allow-Credentials", "true")
        
        return response, 200
        
    except Exception as e:
        print(f"Error in URL analysis: {str(e)}")
        print(traceback.format_exc())
        
        error_response = jsonify({
            "error": "Failed to analyze URL",
            "message": str(e)
        })
        error_response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
        
        return error_response, 500

@bp.after_request
def after_request(response):
    """Ensure CORS headers are added to all responses"""
    origin = request.headers.get("Origin")
    if origin in ["https://url-email-phishing-detection.vercel.app", "http://localhost:3000", "http://localhost:4200"]:
        response.headers.add("Access-Control-Allow-Origin", origin)
    else:
        response.headers.add("Access-Control-Allow-Origin", "*")
    
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, Accept")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    
    return response