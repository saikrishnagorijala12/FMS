from http.client import responses

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from fms.services import analytics

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@analytics_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard_analytics():
    response, status = analytics.get_dashboard()
    return jsonify(response), status


@analytics_bp.route('/sales', methods=['GET'])
@jwt_required()
def get_sales_analytics():
    data = request.json
    response, status = analytics.get_sales(data)
    return jsonify(response), status

@analytics_bp.route('/inventory', methods=['GET'])
@jwt_required()
def inventory_analytics():
    response, status =analytics.get_inventory_data()
    return jsonify(response), status

@analytics_bp.route('/customers', methods=['GET'])
@jwt_required()
def customer_analytics():
    response, status =analytics.get_customer_data()
    return jsonify(response), status


@analytics_bp.route('/franchises', methods=['GET'])
@jwt_required()
def franchise_performance():
    claims = get_jwt()
    if claims.get("role_name") != "Franchisor":
        return jsonify({"msg": "Unauthorized"}), 403
    response, status = analytics.get_franchise_performance()
    return jsonify(response), status