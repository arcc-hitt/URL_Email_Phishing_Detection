from flask import Blueprint, request, jsonify
from services.email_service import EmailService

bp = Blueprint("email_analysis", __name__)
email_service = EmailService()

@bp.route("/analyze", methods=["POST"])
def analyze_email():
    email_data = request.json
    result = email_service.analyze_email(email_data)
    return jsonify(result)
