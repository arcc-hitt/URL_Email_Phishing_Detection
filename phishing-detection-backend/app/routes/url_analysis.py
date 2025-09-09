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

@bp.route("/analyze", methods=["POST"])
def analyze_url():
    try:
        url = request.json.get("url", "")
        if not url:
            return jsonify({"error": "URL is required"}), 400
            
        service = get_url_service()
        result = service.analyze_url(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
