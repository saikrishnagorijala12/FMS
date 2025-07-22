from http.client import responses

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from fms.models import Customer
from fms.services import customer

customer_bp = Blueprint('customers', __name__, url_prefix='/customers')

@customer_bp.route('', methods=['GET'])
@jwt_required()
def get_customers():
    claims = get_jwt()
    role = claims.get("role_name")
    if role not in ["Franchisor", "Franchisee"]:
        return jsonify({"msg": "Unauthorized"}), 403
    response, status = customer.get_customers()
    return jsonify(response), status

@customer_bp.route('/<int:customer_id>', methods=['GET'])
@jwt_required()
def get_customer_details(customer_id):
   response, status = customer.get_customer_details(customer_id)
   return jsonify(response), status

@customer_bp.route('/<int:customer_id>/orders', methods=['GET'])
@jwt_required()
def get_customer_orders(customer_id):
    response, status = customer.get_customer_orders(customer_id)
    return jsonify(response), status

@customer_bp.route('/<int:customer_id>/address', methods=['GET'])
@jwt_required()
def get_customer_address_route(customer_id):
    response, status = customer.fetch_customer_address(customer_id)
    return jsonify(response), status

@customer_bp.route('/<int:user_id>/address', methods=['POST'])
@jwt_required()
def update_customer_address_route(user_id):
    data = request.json
    response, status = customer.post_customer_address(user_id, data)
    return jsonify(response), status

@customer_bp.route('/<int:customer_id>/status', methods=['PUT'])
@jwt_required()
def update_customer_status(customer_id):
    data = request.json
    response, status = customer.update_customer_status(customer_id, data)
    return jsonify(response), status
