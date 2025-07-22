from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from fms.services import reports

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/sales', methods=['GET'])
@jwt_required()
def sales_report():
    response, status = reports.generate_sales_report()
    return jsonify(response), status


@reports_bp.route('/inventory', methods=['GET'])
@jwt_required()
def inventory_report():
    response, status = reports.generate_inventory_report()
    return jsonify(response), status


@reports_bp.route('/financial', methods=['GET'])
@jwt_required()
def financial_report():
    response, status = reports.generate_financial_report()
    return jsonify(response), status