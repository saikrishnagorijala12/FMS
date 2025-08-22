from http.client import responses

from fms import db
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from fms.models import  Product, Franchisor, User
from fms.utils import role_required
from fms.services import products

products_bp = Blueprint('products', __name__,url_prefix='/products')


@products_bp.route('',methods=['POST'])
@jwt_required
def create_product():
    data=request.json
    response, status = products.new_product(data)
    return jsonify(response), status


@products_bp.route('', methods=['GET'])
@jwt_required()
def get_all_products():
    response, status = products.list_products()
    return jsonify(response), status


@products_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    response, status = products.get_product(product_id)
    return jsonify(response), status


@products_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    claims = get_jwt()
    if claims.get("role_name") != "franchisor":
        return jsonify({"error": "Unauthorized"}), 403
    franchisor_id = claims.get("franchisor_id")
    if not franchisor_id:
        return jsonify({"error": "Missing franchisor_id in token"}), 403
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    if str(product.franchisor_id) != franchisor_id:
        return jsonify({"error": "You are not authorized to modify this product"}), 403

    data = request.get_json()
    response, status = update_product(product_id, data)
    return jsonify(response), status


@products_bp.route("/<int:product_id>",methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    claims = get_jwt()

    if claims["role_name"] != "franchisor":
        return jsonify({"error": "Only franchisors can delete products."}), 403

    product = Product.query.filter_by(product_id=product_id).first()

    if not product:
        return jsonify({"error": "Product not found."}), 404

    if str(product.franchisor_id) != str(claims.get("franchisor_id")):
        return jsonify({"error": "You are not authorized to delete this product."}), 403

    response, status = products.delete_product(product_id)
    return jsonify(response), status

