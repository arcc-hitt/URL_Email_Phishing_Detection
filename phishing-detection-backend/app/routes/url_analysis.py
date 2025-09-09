import logging
from flask import Blueprint, request, jsonify, current_app
from app.services.url_service import URLService

bp = Blueprint("url_analysis", __name__)
logger = logging.getLogger(__name__)

# Initialize service as None - will be lazy loaded
url_service = None

def get_url_service():
    global url_service
    if url_service is None:
        try:
            logger.info("Initializing URL service...")
            url_service = URLService()
            logger.info("URL service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize URL service: {e}")
            raise e
    return url_service

@bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for URL analysis service"""
    try:
        service = get_url_service()
        return jsonify({
            "status": "healthy",
            "service": "url_analysis",
            "message": "URL analysis service is running"
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "service": "url_analysis",
            "error": str(e)
        }), 500

@bp.route("/analyze", methods=["POST"])
def analyze_url():
    try:
        # Validate request
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        url = data.get("url", "").strip()
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        # Basic URL validation
        if not (url.startswith("http://") or url.startswith("https://")):
            return jsonify({"error": "URL must start with http:// or https://"}), 400
        
        logger.info(f"Analyzing URL: {url[:50]}...")
        
        # Get service and analyze URL
        service = get_url_service()
        result = service.analyze_url(url)
        
        logger.info(f"Analysis completed for URL: {url[:50]}...")
        return jsonify(result)
        
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error analyzing URL: {e}")
        return jsonify({"error": "Internal server error occurred during analysis"}), 500
