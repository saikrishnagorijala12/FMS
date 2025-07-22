from flask import Blueprint, request, jsonify
from fms.services.browse import browse_categories_service, browse_franchises_service

browse_bp = Blueprint('browse', __name__, url_prefix='/browse')

@browse_bp.route('/categories', methods=['GET'])
def browse_categories():
    result = browse_categories_service()
    return jsonify(result), 204


@browse_bp.route('/franchises', methods=['GET'])
def browse_franchises():
    region = request.args.get('region', '')
    result = browse_franchises_service(region)
    return jsonify(result), 200
