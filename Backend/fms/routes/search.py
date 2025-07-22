from flask import Blueprint, request, jsonify
from fms.services.search import search_products_service, search_franchises_service

search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('/products', methods=['GET'])
def search_products():
    keyword = request.args.get('q', '')
    if not keyword:
        return jsonify({'error': 'Missing search query `q`'}), 400
    result = search_products_service(keyword)
    return jsonify(result), 200


@search_bp.route('/franchises', methods=['GET'])
def search_franchises():
    location = request.args.get('location', '')
    if not location:
        return jsonify({'error': 'Missing `location` parameter'}), 400
    result = search_franchises_service(location)
    return jsonify(result), 200
