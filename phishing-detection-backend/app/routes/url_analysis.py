from flask import Blueprint, request, jsonify
from app.services.url_service import URLService
from app.services.simple_url_service import SimpleURLService
import logging

bp = Blueprint("url_analysis", __name__)
logger = logging.getLogger(__name__)

# Initialize service as None to lazy load it
url_service = None
simple_service = None

def get_url_service():
    global url_service, simple_service
    
    # Try to use the full service first
    if url_service is None:
        try:
            url_service = URLService()
            if URLService.models_ready():
                logger.info("Using full URL service with both models")
                return url_service
        except Exception as e:
            logger.warning(f"Full URL service failed, trying simple service: {e}")
    
    # Fallback to simple service
    if simple_service is None:
        try:
            simple_service = SimpleURLService()
            SimpleURLService.preload_models()
            logger.info("Using simple URL service (XGBoost only)")
        except Exception as e:
            logger.error(f"Simple URL service also failed: {e}")
            raise e
    
    return simple_service

@bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint that doesn't require model loading"""
    try:
        full_service_ready = URLService.models_ready()
        simple_service_ready = SimpleURLService.models_ready()
        
        any_service_ready = full_service_ready or simple_service_ready
        
        return jsonify({
            "status": "healthy" if any_service_ready else "loading",
            "full_service_ready": full_service_ready,
            "simple_service_ready": simple_service_ready,
            "models_loaded": any_service_ready
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
