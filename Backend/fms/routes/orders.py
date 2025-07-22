from flask import Blueprint, jsonify,request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from fms.services import orders

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    claims = get_jwt()
    role_name = claims.get("role_name")
    if role_name != "Customer":
        return jsonify({"message": "Only customers can create orders"}), 403

    data = request.get_json()
    response, status = orders.create_order(data)
    return jsonify(response), status


@orders_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_orders_by_user(user_id):
    response, status = orders.get_order_by_user(user_id)
    return jsonify(response), status

@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    claims = get_jwt()
    role_name = claims.get("role_name").lower()
    user_id = get_jwt_identity()

    response, status = orders.get_orders_by_role(role_name, user_id)
    return jsonify(response), status


@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order_by_id(order_id):
    claims = get_jwt()
    role_name = claims.get("role_name").lower()
    user_id = get_jwt_identity()

    response, status = orders.get_order_by_id(order_id, role_name, user_id)
    return jsonify(response), status


@orders_bp.route('/<int:order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    data = request.json
    new_status = data.get("status_id")
    claims = get_jwt()
    user_id = get_jwt_identity()

    if claims.get("role_name").lower() != "franchisee":
        return jsonify({"message": "Unauthorized"}), 403

    response, status = orders.update_order_status(order_id, user_id, new_status)
    return jsonify(response), status


@orders_bp.route('/<int:order_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_order(order_id):
    claims = get_jwt()
    user_id = get_jwt_identity()

    if claims.get("role_name").lower() != "customer":
        return jsonify({"message": "Unauthorized"}), 403

    response, status = orders.cancel_order(order_id, user_id)
    return jsonify(response), status


@orders_bp.route('/<int:order_id>/tracking', methods=['GET'])
@jwt_required()
def get_tracking(order_id):
    claims = get_jwt()
    user_id = get_jwt_identity()

    response, status = orders.get_tracking_info(order_id, claims['role_name'].lower(), user_id)
    return jsonify(response), status


@orders_bp.route('/<int:order_id>/items', methods=['POST'])
@jwt_required()
def add_order_item(order_id):
    data = request.json
    claims = get_jwt()
    user_id = get_jwt_identity()

    if claims['role_name'].lower() != 'customer':
        return jsonify({"message": "Unauthorized"}), 403

    response, status = orders.add_order_item(order_id, user_id, data)
    return jsonify(response), status


@orders_bp.route('/<int:order_id>/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_order_item(order_id, item_id):
    claims = get_jwt()
    user_id = get_jwt_identity()

    if claims['role_name'].lower() != 'customer':
        return jsonify({"message": "Unauthorized"}), 403

    response, status = orders.remove_order_item(order_id, item_id, user_id)
    return jsonify(response), status


@orders_bp.route('/all', methods=['GET'])
@jwt_required()
def product_sales():
    data, status = orders.get_product_sales()
    return jsonify(data), status