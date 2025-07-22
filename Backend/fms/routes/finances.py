from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from fms.services import finances

finances_bp = Blueprint("finances", __name__, url_prefix="/finances")

@finances_bp.route("/commissions", methods=["GET"])
@jwt_required()
def get_commissions():
    user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims.get("role_name")

    response, status = finances.get_commissions(user_id, role)
    return jsonify(response), status

@finances_bp.route("/earnings", methods=["GET"])
@jwt_required()
def get_earnings():
    user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims.get("role_name")

    response, status = finances.get_earnings(user_id, role)
    return jsonify(response), status

@finances_bp.route("/withdraw", methods=["POST"])
@jwt_required()
def request_withdrawal():
    user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims.get("role_name")

    if role != "Franchisee":
        return jsonify({"msg": "Only franchisees can request withdrawal"}), 403

    data = request.get_json()
    response, status = finances.request_withdrawal(user_id, data)
    return jsonify(response), status

@finances_bp.route("/withdrawals", methods=["GET"])
@jwt_required()
def get_withdrawals():
    response, status = finances.get_withdrawl_request()
    return jsonify(response), status