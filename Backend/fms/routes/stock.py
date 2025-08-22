from flask import Blueprint, jsonify,request
from flask_jwt_extended import jwt_required, get_jwt
from fms.services import stock

stock_bp = Blueprint('stocks', __name__, url_prefix='/stocks')

# @stock_bp.route('/<int:franchisor_id>', methods=['POST'])
# @jwt_required()
# def request_stock(franchisor_id):
#     # data = request.json
#     # response, status = stock.add_product(data)
#     # return jsonify(response), status


@stock_bp.route('/<int:franchisor_id>', methods=['GET'])
@jwt_required()
def get_stocks(franchisor_id):
    data, status = stock.get_products_list(franchisor_id)
    return jsonify(data), status

@stock_bp.route('/add', methods=['POST'])
@jwt_required()
def add_products():
    data = request.json
    response, status = stock.add_new_product(data)
    return jsonify(response), status

@stock_bp.route('/update_stock/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_stocks(product_id):
    data = request.json
    response, status = stock.update_product(data,product_id)
    return jsonify(response), status


@stock_bp.route('/update_price/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product_price(product_id):
    data = request.json
    response, status = stock.update_price(data,product_id)
    return jsonify(response), status


@stock_bp.route('/delete/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    response, status = stock.deleteProduct(product_id)
    return jsonify(response), status
