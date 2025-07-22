from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from fms.services import notification

notification_bp = Blueprint("notifications", __name__, url_prefix="/notifications")

@notification_bp.route('', methods=['GET'])
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()
    response, status =notification.get_user_notifications(user_id)
    return jsonify(response), status

@notification_bp.route('/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_notification_read(notification_id):
    user_id = get_jwt_identity()
    response, status =notification.mark_as_read(user_id, notification_id)
    return jsonify(response), status

@notification_bp.route('/read-all', methods=['PUT'])
@jwt_required()
def mark_all_read():
    user_id = get_jwt_identity()
    response, status =notification.mark_all_as_read(user_id)
    return jsonify(response), status

@notification_bp.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    user_id = get_jwt_identity()
    response, status =notification.delete_notification(user_id, notification_id)
    return jsonify(response), status
