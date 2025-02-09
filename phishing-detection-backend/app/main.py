import datetime
from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from config import config

mongodb_uri = config.MONGODB_URI
client = MongoClient(mongodb_uri)
db = client["phishing_detection_db"]
logs_collection = db['phishing_logs']

bp = Blueprint('logs_api', __name__)

@bp.route('/api/phishing_logs', methods=['POST'])
def save_log():
    log_data = request.json
    log_data['created_at'] = datetime.datetime.now()
    logs_collection.insert_one(log_data)
    return jsonify({"message": "Log saved successfully"}), 201

@bp.route('/api/phishing_logs', methods=['GET'])
def get_logs():
    logs = list(logs_collection.find())
    for log in logs:
        log["_id"] = str(log["_id"])
    return jsonify(logs), 200
