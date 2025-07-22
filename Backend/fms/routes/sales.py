from http.client import responses

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required,get_jwt
from fms.services import sales

sales_bp = Blueprint('sales', __name__, url_prefix='/sales')

@sales_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_sale_for(user_id):
    response, status = sales.get_sales_data(user_id)
    return jsonify(response), status

@sales_bp.route('/<int:user_id>/unpaid', methods=['GET'])
@jwt_required()
def get_unpaid_commisons(user_id):
    response, status = sales.getUnpaidCommisions(user_id)
    return jsonify(response), status