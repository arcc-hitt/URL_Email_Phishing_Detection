from flask import Blueprint, request, jsonify
from app.services.url_service import URLService

bp = Blueprint("url_analysis", __name__)
url_service = URLService()

@bp.route("/analyze", methods=["POST", "OPTIONS"])
def analyze_url():
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight successful"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response, 200

    url = request.json.get("url", "")
    result = url_service.analyze_url(url)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
