from flask import Blueprint, request, jsonify
from app.services.url_service import URLService

bp = Blueprint("url_analysis", __name__)

# Initialize service as None to lazy load it
url_service = None

def get_url_service():
    global url_service
    if url_service is None:
        url_service = URLService()
    return url_service

@bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint that doesn't require model loading"""
    try:
        models_ready = URLService.models_ready()
        return jsonify({
            "status": "healthy" if models_ready else "loading",
            "models_loaded": models_ready
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "models_loaded": False
        }), 500

@bp.route("/analyze", methods=["POST"])
def analyze_url():
    try:
        # Check if request has JSON data
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        url = data.get("url", "")
        if not url:
            return jsonify({"error": "URL is required"}), 400
            
        service = get_url_service()
        result = service.analyze_url(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
