from flask import Blueprint, request, jsonify
from app.services.email_service import EmailService

bp = Blueprint("email_analysis", __name__)
email_service = EmailService()

@bp.route("/analyze", methods=["POST", "OPTIONS"])
def analyze_email():
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight successful"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response, 200

    email_data = request.json
    result = email_service.analyze_email(email_data)
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
