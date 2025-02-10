from flask import Blueprint, request, jsonify
from app.services.url_service import URLService

bp = Blueprint("url_analysis", __name__)
url_service = URLService()

@bp.route("/analyze", methods=["POST"])
def analyze_url():
    url = request.json.get("url", "")
    result = url_service.analyze_url(url)
    return jsonify(result)