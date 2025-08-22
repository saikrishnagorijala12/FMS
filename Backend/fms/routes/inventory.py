from flask import Blueprint, jsonify,request
from flask_jwt_extended import jwt_required, get_jwt
from fms.services import inventory

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_inventory_route(user_id):
    claims = get_jwt()
    role_name = claims.get("role_name")
    print(role_name)

    # if role_name not in ["Franchisor","Franchisee", "Admin"]:
    #     return jsonify({"message": "Unauthorized"}), 403

    response, status = inventory.get_inventory(user_id)
    return jsonify(response), status

@inventory_bp.route('/franchisee/<int:user_id>', methods=['GET'])
@jwt_required()
def get_inventory_route_franchisee(user_id):
    claims = get_jwt()
    role_name = claims.get("role_name")
    print(role_name)

    # if role_name not in ["Franchisor","Franchisee", "Admin"]:
    #     return jsonify({"message": "Unauthorized"}), 403

    response, status = inventory.get_inventory_franchisee(user_id)
    return jsonify(response), status

@inventory_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_inventory(product_id):
    data = request.json
    response, status = inventory.update_inventory(product_id,data)
    return jsonify(response), status

@inventory_bp.route('/stock-request', methods=['POST'])
@jwt_required()
def request_stock():
    data = request.json
    response, status = inventory.stock_request(data)
    return jsonify(response), status


@inventory_bp.route('/stock-requests', methods=['GET'])
@jwt_required()
def get_stock_requests():
    claims = get_jwt()
    role_name = claims.get("role_name")

    if role_name not in ["Franchisor","Franchisee", "Admin"]:
        return jsonify({"message": "Unauthorized"}), 403

    response, status = inventory.get_all_stock_requests()
    return jsonify(response), status


@inventory_bp.route('/stock-requests/<int:request_id>/approve', methods=['PUT'])
@jwt_required()
def approve_stock_request(request_id):
    claims = get_jwt()
    role_name = claims.get("role_name")
    print(role_name)

    if role_name not in ["Franchisor", "Admin"]:
        return jsonify({"message": "Unauthorized"}), 403

    response, status = inventory.approve_stock_request(request_id)
    return jsonify(response), status


@inventory_bp.route('/stock-requests/<int:request_id>/reject', methods=['PUT'])
@jwt_required()
def reject_stock_request(request_id):
    claims = get_jwt()
    role_name = claims.get("role_name")

    if role_name not in ["Franchisor", "Admin"]:
        return jsonify({"message": "Unauthorized"}), 403

    response, status = inventory.reject_stock_request(request_id)
    return jsonify(response), status


@inventory_bp.route('/stock-requests/<int:request_id>/ship', methods=['PUT'])
@jwt_required()
def ship_stock_request(request_id):
    claims = get_jwt()
    role_name = claims.get("role_name")

    if role_name != "Franchisor":
        return jsonify({"message": "Only franchisors can mark stock as shipped"}), 403

    response, status = inventory.ship_stock_request(request_id)
    return jsonify(response), status


@inventory_bp.route('/stock-requests/<int:request_id>/delivered', methods=['PUT'])
@jwt_required()
def mark_stock_request_delivered(request_id):
    claims = get_jwt()
    role_name = claims.get("role_name")

    if role_name != "Franchisor":
        return jsonify({"message": "Only franchisors can mark stock as delivered"}), 403

    response, status = inventory.mark_stock_delivered(request_id)
    return jsonify(response), status
