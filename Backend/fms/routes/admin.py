from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from fms.services import admin as admin_service

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    claims = get_jwt()
    if claims.get("role_name") != "Admin":
        return jsonify({"msg": "Unauthorized"}), 403
    response, status = admin_service.get_all_users()
    return jsonify(response), status

@admin_bp.route('/system-stats', methods=['GET'])
@jwt_required()
def get_system_stats():
    claims = get_jwt()
    if claims.get("role_name") != "Admin":
        return jsonify({"msg": "Unauthorized"}), 403
    response, status = admin_service.get_system_stats()
    return jsonify(response), status

@admin_bp.route('/audit-logs', methods=['GET'])
@jwt_required()
def get_audit_logs():
    claims = get_jwt()
    if claims.get("role_name") != "Admin":
        return jsonify({"msg": "Unauthorized"}), 403
    response, status = admin_service.get_audit_logs()
    return jsonify(response), status

@admin_bp.route('/notifications/broadcast', methods=['POST'])
@jwt_required()
def send_broadcast_notification():
    claims = get_jwt()
    if claims.get("role_name") != "Admin":
        return jsonify({"msg": "Unauthorized"}), 403
    data = request.json
    response, status = admin_service.send_broadcast_notification(data)
    return jsonify(response), status

@admin_bp.route('/settings', methods=['GET', 'PUT'])
@jwt_required()
def system_settings():
    claims = get_jwt()
    if claims.get("role_name") != "Admin":
        return jsonify({"msg": "Unauthorized"}), 403

    if request.method == 'GET':
        response, status = admin_service.get_settings()
    else:
        data = request.json
        response, status = admin_service.update_settings(data)
    return jsonify(response), status
